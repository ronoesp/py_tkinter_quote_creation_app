import tkinter as tk
from DB.table_data_model import SettingsData, QuotationBaseData, QuotationDetailData

class AppDataManager:
    # データベース関連：データ共有用変数群
    settings_data: SettingsData = None
    quotation_base_data: QuotationBaseData = None
    quotation_detail_data_list: list[QuotationDetailData] = []
    
    # 作成=False / 編集=True
    edit_mode_flg = False
    
    # now_mode_name = "" #作成、編集、の２つが入る予定（SceneCompleteで使用想定）
    decide_result = False #確認画面で押されたボタンの結果を入れる
    
    # 見積作成で設定したデータの一時保存用変数
    mitumori_no = 1
    
    #見積履歴テストデータ保存用変数
    app_quote_list = []
    
    @classmethod
    def init(cls, root: tk.Tk):
        cls.decide_result = tk.BooleanVar(master=root, value=False) # サブウィンドウが開いたところで処理を止めるために必要
        
    @classmethod
    def append_quote_data(cls, quote_data):
        cls.app_quote_list.append(quote_data)
        
    # 一時保存していた見積/明細データをリセットする
    @classmethod
    def reset_temporary_data(cls):
        cls.quotation_base_data = None
        cls.quotation_detail_data_list = []