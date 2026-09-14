
class TableDefine():
    # テーブル定義用の辞書作成：設定情報テーブル
    @classmethod
    def table_define_dict_setttings(self):
        order = []
        order.append({"name" : "settings_id", "type" : "INTEGER", "constraints" : "PRIMARY KEY CHECK (settings_id = 1)"})
        order.append({"name" : "tax_rate", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "delete_grace_days", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "company_name", "type" : "TEXT", "constraints" : "NOT NULL"})
        order.append({"name" : "company_address", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "company_phone", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "company_contact_name", "type" : "TEXT", "constraints" : ""})
        return {"table_name": "settings", "columns": order}
        
    # テーブル定義用の辞書作成：見積基本情報テーブル
    @classmethod
    def table_define_dict_quotation_base(self):
        order = []
        order.append({"name" : "quotation_id", "type" : "INTEGER", "constraints" : "PRIMARY KEY AUTOINCREMENT"})
        order.append({"name" : "quotation_number", "type" : "TEXT", "constraints" : "NOT NULL"})
        order.append({"name" : "created_date", "type" : "TEXT", "constraints" : "NOT NULL"})
        order.append({"name" : "subject", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "valid_until", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "client_company_name", "type" : "TEXT", "constraints" : "NOT NULL"})
        order.append({"name" : "client_contact_name", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "notes", "type" : "TEXT", "constraints" : ""})
        return {"table_name": "quotation_base", "columns": order}
        
    # テーブル定義用の辞書作成：明細情報テーブル
    @classmethod
    def table_define_dict_quotation_detail(self):
        order = []
        order.append({"name" : "item_id", "type" : "INTEGER", "constraints" : "PRIMARY KEY AUTOINCREMENT"})
        order.append({"name" : "quotation_id", "type" : "INTEGER", "constraints" : "NOT NULL REFERENCES quotation_base_info(quotation_id)"})
        order.append({"name" : "item_name", "type" : "TEXT", "constraints" : "NOT NULL"})
        order.append({"name" : "unit", "type" : "TEXT", "constraints" : ""})
        order.append({"name" : "unit_price", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "quantity", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "tax_rate", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "amount", "type" : "INTEGER", "constraints" : "NOT NULL"})
        order.append({"name" : "description", "type" : "TEXT", "constraints" : ""})
        return {"table_name": "quotation_detail", "columns": order}
    
    @classmethod
    def table_define_dict_list(self):
        dict_list = [self.table_define_dict_setttings(),
                     self.table_define_dict_quotation_base(),
                     self.table_define_dict_quotation_detail()]
        return dict_list