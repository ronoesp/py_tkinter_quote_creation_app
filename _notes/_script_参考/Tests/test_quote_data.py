from quote_data import *
from app_data_manager import AppDataManager as app_data

# gui_managerから呼んで動作テストしている
class TestQuotedata():
    def __init__(self):
        self.main()
    
    def test_quote_data_a(self):
        # ---- テスト用データ(将来的にはDBのSELECT結果に置き換わる部分) ----
        quote_dict = {
            "tax_rate": 5,
            "deletion_date": "2027-01-01",
            "our_company_manager": "山田太郎",
            "create_date": "2026-08-12",
            "quote_id": 1,
            "subject": "システム開発費用",
            "contract_expiration_date": "2026-09-30",
            "recipient_company_name": "株式会社サンプル",
            "recipient_manager_name": "鈴木一郎",
            "remarks": "特になし",
        }
        return quote_dict

    def test_quote_data_b(self):
        # ---- テスト用データ(将来的にはDBのSELECT結果に置き換わる部分) ----
        quote_dict = {
            "tax_rate": 10,
            "deletion_date": "2027-01-01",
            "our_company_manager": "山田太郎",
            "create_date": "2024-08-12",
            "quote_id": 2,
            "subject": "システム開発費用",
            "contract_expiration_date": "2026-09-30",
            "recipient_company_name": "株式会社ギャンブル",
            "recipient_manager_name": "水谷一平",
            "remarks": "特になし",
        }
        return quote_dict

    def test_quote_data_c(self):
        # ---- テスト用データ(将来的にはDBのSELECT結果に置き換わる部分) ----
        quote_dict = {
            "tax_rate": 10,
            "deletion_date": "2027-01-01",
            "our_company_manager": "山田太郎",
            "create_date": "2025-08-12",
            "quote_id": 3,
            "subject": "システム開発費用",
            "contract_expiration_date": "2026-09-30",
            "recipient_company_name": "株式会社サンプル",
            "recipient_manager_name": "小野良哉",
            "remarks": "特になし",
        }
        return quote_dict

    def test_detail_data_a(self):
        detail_dict_a = {"item_name": "商品A", 
                        "unit": "個", 
                        "unit_price": 1000, 
                        "quantity": 5, 
                        "amount": 5000, 
                        "description": "食品"}
        
        detail_dict_b = {"item_name": "商品B", 
                                "unit": "個", 
                                "unit_price": 100, 
                                "quantity": 500, 
                                "amount": 50000, 
                                "description": "食品"}

        detail_list = []
        detail_list.append(detail_dict_a)
        detail_list.append(detail_dict_b)

        # detail_list = [
        #     {"item_name": "商品A", "unit": "個", "unit_price": 1000, "quantity": 5, "amount": 5000, "description": "説明文"},
        #     {"item_name": "商品B", "unit": "本", "unit_price": 500, "quantity": 3, "amount": 1500, "description": ""},
        # ]
        
        return detail_list

    def test_detail_data_b(self):

        detail_dict = {"item_name": "商品C", 
                        "unit": "本", 
                        "unit_price": 500, 
                        "quantity": 3, 
                        "amount": 1500, 
                        "description": "ライトノベル"}

        detail_list = []
        detail_list.append(detail_dict)

        return detail_list

    def test_detail_data_c(self):

        detail_dict = {"item_name": "商品D", 
                        "unit": "枚", 
                        "unit_price": 120, 
                        "quantity": 1, 
                        "amount": 120, 
                        "description": "高級紙"}

        detail_list = []
        detail_list.append(detail_dict)

        return detail_list

    def main(self):
        # ---- インスタンス化してデータを流し込む ----
        quote_a = QuoteData()
        quote_b = QuoteData()
        quote_c = QuoteData()
        quote_a.load_from_dict(self.test_quote_data_a(), self.test_detail_data_a())
        quote_b.load_from_dict(self.test_quote_data_b(), self.test_detail_data_b())
        quote_c.load_from_dict(self.test_quote_data_c(), self.test_detail_data_c())
        
        # AppDataManagerクラスに保存
        app_data.append_quote_data(quote_a)
        app_data.append_quote_data(quote_b)
        app_data.append_quote_data(quote_c)
        
        print("データ数： " + str(len(app_data.app_quote_list)))
        print("======================================")

        # ---- 確認 ----
        for quote in app_data.app_quote_list:
            print(quote.subject)
            print(len(quote.detail_data_list))
            for detail in quote.detail_data_list:
                print(detail.item_name, detail.amount)
            print("======================================")
        
        
        # print(quote_a.subject)
        # print(len(quote_a.detail_data_list))
        # for detail in quote_a.detail_data_list:
        #     print(detail.item_name, detail.amount)
            
        # print(quote_b.subject)
        # print(len(quote_b.detail_data_list))
        # for detail in quote_b.detail_data_list:
        #     print(detail.item_name, detail.amount)
            
        # print(quote_c.subject)
        # print(len(quote_c.detail_data_list))
        # for detail in quote_c.detail_data_list:
        #     print(detail.item_name, detail.amount)
        
test = TestQuotedata()

# ※将来DBに差し替えるときのイメージ
# sqlite3.Rowはdict(row)とすることで簡単に辞書へ変換できるため、
# テストで使っていたload_from_dictのロジックをそのまま流用できます。
# これが「辞書型で用意しておくと、DB接続時の移行がスムーズ」という意味です。
# ============================================================================
# def fetch_quote_from_db(quote_id: int) -> QuoteData:
#     conn = sqlite3.connect("quote.db")
#     conn.row_factory = sqlite3.Row
    
#     row = conn.execute("SELECT * FROM quote_data WHERE quote_id = ?", (quote_id,)).fetchone()
#     detail_rows = conn.execute("SELECT * FROM detail_data WHERE quote_id = ?", (quote_id,)).fetchall()
    
#     quote = QuoteData()
#     quote.load_from_dict(dict(row), [dict(r) for r in detail_rows])  # ★sqlite3.Rowをdictに変換するだけ
    
#     conn.close()
#     return quote
# ============================================================================