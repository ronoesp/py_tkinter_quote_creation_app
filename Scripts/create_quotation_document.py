from app_data_manager import AppDataManager as app_data
from DB.table_data_model import SettingsData, QuotationBaseData, QuotationDetailData
from DB.data_base_controller import DatabaseController

class CreateQuotationDocument:
    
    @classmethod
    def create_detail_text(cls):
        detail_data_list = app_data.quotation_detail_data_list
        l_text = ""
        
        for data in detail_data_list:
            l_text = l_text + "============================" + "\n"
            # l_text = l_text + "明細番号：" + "\n"
            l_text = l_text + "摘要　　：" + data.item_name + "\n"
            l_text = l_text + "単価　　：" + str(data.unit_price) + "\n"
            l_text = l_text + "数量　　：" + str(data.quantity) + "\n"
            l_text = l_text + "金額　　：" + str(data.amount) + "\n" #金額計算用の関数を作成する？
            
        l_text = l_text + "============================" + "\n"
        
        return l_text
    
    
    @classmethod
    def calc_total_amount(cls, add_tax_flg: bool = False):
        detail_data_list = app_data.quotation_detail_data_list
        total = 0
        
        for data in detail_data_list:
            price = int(data.unit_price)
            quantity = int(data.quantity)
            
            rate = 100
            if add_tax_flg:
                rate = rate + int(data.tax_rate)
            
            total = total + ( ( price * quantity ) * rate ) / 100
            
        # ※どれを使うかは要件次第（今回は切り捨て）
        # ========================
        # 切り捨て
        total = int(total)

        # 四捨五入
        # total = round(total)

        # 切り上げ
        # import math
        # total = math.ceil(total)
        # ========================
        
        return total
        

    # AppDataManagerクラスのデータから文章を組み立てる
    @classmethod
    def create_text(cls):
        setting_data = app_data.settings_data
        quate_data = app_data.quotation_base_data
        # detail_data_list = app_data.quotation_detail_data_list
        
        l_text = ""
        
        l_text = l_text + "御見積書" + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "見積番号：" + quate_data.quotation_number + "\n"
        l_text = l_text + "作成日　：" + quate_data.created_date + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "自社名　　　：" + setting_data.company_name + "\n"
        l_text = l_text + "自社住所　　：" + setting_data.company_address + "\n"
        l_text = l_text + "自社電話番号：" + setting_data.company_phone + "\n"
        l_text = l_text + "自社担当者名：" + setting_data.company_contact_name + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "件名　　：" + quate_data.subject + "\n"
        l_text = l_text + "有効期限：" + quate_data.valid_until + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "宛先会社名　：" + quate_data.client_company_name + "\n"
        l_text = l_text + "宛先担当者名：" + quate_data.client_contact_name + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "合計金額：" + "\n" #※合計金額を出す関数を作成後に対応
        l_text = l_text + "\n"
        l_text = l_text + "内訳：" + "\n"
        
        l_text = l_text + cls.create_detail_text()
        
        total = cls.calc_total_amount()
        total_add_tax = cls.calc_total_amount(True)
        tax_only = total_add_tax - total
        
        l_text = l_text + "価格　　：" + str(total) + "\n"
        l_text = l_text + "税　　　：" + str(tax_only) + "\n"
        l_text = l_text + "税込価格：" + str(total_add_tax) + "\n"
        l_text = l_text + "============================" + "\n"
        l_text = l_text + "\n"
        l_text = l_text + "備考　：" + quate_data.notes + "\n"
        # l_text = l_text + quate_data.notes + "\n"
        
        return l_text
        
        
        # 【予定形式】
        # CSV形式
        
        # 御見積書
        # 
        # 見積番号：＊＊＊
        # 作成日　：＊＊＊
        # 
        # 自社名　　　：
        # 自社住所　　：
        # 自社電話番号：
        # 自社担当者名：
        # 
        # 件名　　：
        # 有効期限：
        # 
        # 宛先会社名　：
        # 宛先担当者名：
        # 
        # 合計金額：＊＊＊＊＊＊＊
        # 
        # 内訳：
        # ============================
        # 明細番号：1
        # 摘要　　：
        # 数量　　：
        # 単価　　：
        # 金額　　：
        # ============================
        # 明細番号：2
        # 摘要　　：
        # 数量　　：
        # 単価　　：
        # 金額　　：
        # ============================
        # 小計　：
        # 消費税：
        # 合計　：
        # ============================
        # 
        # 備考
        # ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
        # ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
        # ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
        # 