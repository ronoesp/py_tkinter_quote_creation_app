import csv
from app_data_manager import AppDataManager as app_data
from tkinter import filedialog
import os



class QuotationCsvExporter():

    @classmethod
    def export(cls):
        
        file_path = cls._set_file_path()
        if file_path == "":
            return False
        
        
        setting_data = app_data.settings_data
        quate_data = app_data.quotation_base_data
        detail_data_list = app_data.quotation_detail_data_list
        
        
        
        total = cls.calc_total_amount()
        total_add_tax = cls.calc_total_amount(True)
        tax_only = total_add_tax - total
        
        
        # writer.writerow([...])を呼ぶたびに、自動的に正しい区切り文字・正しい改行・必要な場合のエスケープが行われます。
        # 「行を分ける」という操作自体は、csvモジュールに任せてしまえば、"\n"を自分で挟む必要すらありません。
        
        with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            writer.writerow(["御見積書"])
            writer.writerow([])
            writer.writerow(["見積番号", quate_data.quotation_number])
            writer.writerow(["作成日", quate_data.created_date])
            writer.writerow([])
            writer.writerow(["自社名", setting_data.company_name])
            writer.writerow(["自社住所", setting_data.company_address])
            writer.writerow(["自社電話番号", setting_data.company_phone])
            writer.writerow(["自社担当者名", setting_data.company_contact_name])
            writer.writerow([])
            writer.writerow(["件名", quate_data.subject])
            writer.writerow(["有効期限", quate_data.valid_until])
            writer.writerow([])
            writer.writerow(["宛先会社名", quate_data.client_company_name])
            writer.writerow(["宛先担当者名", quate_data.client_contact_name])
            writer.writerow([])
            writer.writerow(["内訳"])
            writer.writerow(["品目名", "単価", "数量", "消費税率", "金額"])  # 明細のヘッダー行

            for data in detail_data_list:
                writer.writerow([data.item_name, data.unit_price, data.quantity, data.tax_rate, data.amount])

            writer.writerow([])
            writer.writerow(["価格", str(total)])
            writer.writerow(["税", str(tax_only)])
            writer.writerow(["税込価格", str(total_add_tax)])
            writer.writerow([])
            writer.writerow(["備考", quate_data.notes])
            # writer.writerow([quate_data.notes])
            
        return True
            
            
    # ボタンに設定：ダイアログボックスから保存先（ファイル名含む）を選択＆出力
    # ================================================================================================
    # ※出力ボタンを押したらこれが開かれる、でもいい気がする（パスとファイル名を記入する場所が変わるだけなんだし）
    # ================================================================================================
    @classmethod
    def _set_file_path(cls):
        # ダイアログを開いてパスとファイル名を設定
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")],
        )

        # キャンセルされた場合は何もしない
        if not path:
            return "" 

        dir_path, file_name_with_ext = os.path.split(path)
        file_name, _ext = os.path.splitext(file_name_with_ext)
        file_path = dir_path + "/" + file_name + ".csv"
        # cls.export(file_path)
        
        # TEST=============================
        # print(dir_path)
        # print(file_name_with_ext)
        # print(file_name)
        # print(_ext)
        # ---------------------------------
        # C:/Users/user/Desktop/DataTest
        # New.csv
        # New
        # .csv
        # TEST=============================
        
        return file_path
    
    
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