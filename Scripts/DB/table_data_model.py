from dataclasses import dataclass, astuple, fields
from .data_base_controller import DatabaseController as db_ctr

# astuple()：dataclassのフィールドを定義順にタプルへ変換
# Not Null項目は必ず値を設定させるために、初期値を設定しないようにしている（インスタンス作成時に設定しないとエラーとなる）
#
# 【注意】settingsは主キーが1固定のため、INSERT用とUPDATE用で同じ値の並びを使い回せる。
# しかし quotation_base_info / quotation_detail は主キーがAUTOINCREMENTで自動採番されるため、
# INSERT時（主キーは渡さない）とUPDATE時（WHERE句に主キーが必要）とで値の並びが異なる。
# そのため、主キーをフィールドの最後に持たせ、insert_values() / update_values() で
# INSERT用・UPDATE用それぞれに適した並びを返すようにしている。


# 親クラス：辞書型から各クラス型のインスタンスに変換する機能を持たせる
class FromDictMixin:
    _table_name: str = ""
    _pk_name: str = ""
    
    # 辞書型のレコードを自身のクラス型に変換して返す
    @classmethod
    def from_dict(cls, record: dict):
        field_names = {f.name for f in fields(cls)}
        filtered = {key: value for key, value in record.items() if key in field_names}
        return cls(**filtered)
    
    # 自身のクラス型のリストに変換して返す
    @classmethod
    def load_conversion_all_data(cls):
        records = db_ctr.get_all_records(cls._table_name)
        return [cls.from_dict(record) for record in records]
    
    # 自身のクラス型のリストに変換して返す(完全一致)
    @classmethod
    def load_conversion_select_data(cls, column_name, value):
        records = db_ctr.get_records_by(cls._table_name, column_name, value)
        return [cls.from_dict(record) for record in records]
    
    # 自身のクラス型のリストに変換して返す(部分一致)
    @classmethod
    def load_conversion_serch_data(cls, column_name, value):
        records = db_ctr.search_records(cls._table_name, column_name, value)
        return [cls.from_dict(record) for record in records]


@dataclass
class SettingsData(FromDictMixin):
    _table_name = "settings"
    
    # settings_id : int # テーブルには定義されているが、1以外の値が入らないので、設定用の変数は不要
    tax_rate: int
    delete_grace_days: int
    company_name: str
    company_address: str = ""
    company_phone: str = ""
    company_contact_name: str = ""

    INSERT_SQL = """
        INSERT OR IGNORE INTO settings
            (settings_id, tax_rate, delete_grace_days, company_name, company_address, company_phone, company_contact_name)
        VALUES (1, ?, ?, ?, ?, ?, ?)
    """

    UPDATE_SQL = """
        UPDATE settings
        SET tax_rate = ?, delete_grace_days = ?, company_name = ?, company_address = ?, company_phone = ?, company_contact_name = ?
        WHERE settings_id = 1
    """
    
    EXISTS_SQL = "SELECT COUNT(*) FROM settings WHERE settings_id = 1"

    def insert_values(self):
        return astuple(self)

    def update_values(self):
        return astuple(self)

    def exists_params(self):
        return ()  # settings_idは常に1固定なのでパラメータ不要

    def get_pk(self):
        return 1  # 常に1固定（未作成/作成済みの判定には使わない）

    def set_pk(self, value):
        pass  # settings_idは常に1固定のため何もしない


@dataclass
class QuotationBaseData(FromDictMixin):
    _table_name = "quotation_base"
    
    quotation_number: str
    created_date: str
    client_company_name: str
    subject: str = ""
    valid_until: str = ""
    client_contact_name: str = ""
    notes: str = ""
    quotation_id: int = None  # 主キー。新規作成時はNone、更新時はDBから取得したIDを設定する

    INSERT_SQL = """
        INSERT INTO quotation_base
            (quotation_number, created_date, client_company_name, subject, valid_until, client_contact_name, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    UPDATE_SQL = """
        UPDATE quotation_base
        SET quotation_number = ?, created_date = ?, client_company_name = ?, subject = ?, valid_until = ?, client_contact_name = ?, notes = ?
        WHERE quotation_id = ?
    """
    
    EXISTS_SQL = "SELECT COUNT(*) FROM quotation_base WHERE quotation_id = ?"

    def insert_values(self):
        return astuple(self)[:-1]  # 最後のquotation_idを除いた分だけ渡す（DB側が自動採番するため）

    def update_values(self):
        return astuple(self)  # quotation_idが最後に含まれるので、WHERE句のプレースホルダにそのまま対応する

    def exists_params(self):
        return (self.quotation_id,)

    def get_pk(self):
        return self.quotation_id

    def set_pk(self, value):
        self.quotation_id = value


@dataclass
class QuotationDetailData(FromDictMixin):
    _table_name = "quotation_detail"
    
    quotation_id: int
    item_name: str
    unit_price: int
    quantity: int
    tax_rate: int
    amount: int
    unit: str = ""
    description: str = ""
    item_id: int = None  # 主キー。新規作成時はNone、更新時はDBから取得したIDを設定する

    INSERT_SQL = """
        INSERT INTO quotation_detail
            (quotation_id, item_name, unit, unit_price, quantity, tax_rate, amount, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    UPDATE_SQL = """
        UPDATE quotation_detail
        SET quotation_id = ?, item_name = ?, unit = ?, unit_price = ?, quantity = ?, tax_rate = ?, amount = ?, description = ?
        WHERE item_id = ?
    """
    
    EXISTS_SQL = "SELECT COUNT(*) FROM quotation_detail WHERE item_id = ?"

    def insert_values(self):
        # フィールド定義順(quotation_id, item_name, unit_price, quantity, tax_rate, amount, unit, description)と
        # INSERT_SQLの列順(quotation_id, item_name, unit, unit_price, quantity, tax_rate, amount, description)が
        # 一致していないため、astuple()をそのまま使わず、SQLの列順に合わせて明示的に組み立てる
        return (self.quotation_id, self.item_name, self.unit, self.unit_price,
                self.quantity, self.tax_rate, self.amount, self.description)

    def update_values(self):
        return (self.quotation_id, self.item_name, self.unit, self.unit_price,
                self.quantity, self.tax_rate, self.amount, self.description, self.item_id)
        
    def exists_params(self):
        return (self.item_id,)

    def get_pk(self):
        return self.item_id

    def set_pk(self, value):
        self.item_id = value