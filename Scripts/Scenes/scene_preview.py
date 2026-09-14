import tkinter as tk
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from app_data_manager import AppDataManager as app_data
from create_quotation_document import CreateQuotationDocument as quote_text
from DB.data_base_controller import DatabaseController
from GUI.tkinter_support import TkinterSupport


class ScenePreview(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.init_root_frame()
        
        self.create_top_area()
        self.create_bot_area()
        self.create_mid_area()
        
    def init_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        title = "プレビュー画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)
        
        text = " 戻る "
        self.bot_area.create_button(text, self.return_scene)
        
        text = " 確定 "
        self.bot_area.create_button(text, self.change_scene)
        
    # ==========================================
    # 3. Middleエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_mid_area(self):
        self.mid_area = mid_area(self)
        
        # 空白エリアを作成
        self.mid_area.create_empty_area(50)
        
        # プレビュー画面用のテキストと、テキスト画面を作成する
        self.mid_area.create_frame()
        self.text = self.mid_area.create_text_dark()
        
    # 文章を設定
    def set_text(self):
        text = quote_text.create_text()
        TkinterSupport.set_text_adjust(text, self.text)
            
    # 前の画面に戻る
    def return_scene(self):
        self.master.show_frame("SceneDetailInformation")
        print("明細情報画面に戻ります")
        
    # 完了画面へ移行
    def change_scene(self):
        self.add_db_recode() # データベースに見積情報を追加
        self.master.show_frame("SceneComplete") # メッセージ設定＆シーン変更
        print("見積書を作成しました（未実装）")

    
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        msg = "確定を押して見積書を作成してください。\n修正が必要な場合は戻るを押してください。"
        self.bot_area.update_msg_box(msg)
        self.set_text()
        
    
    def add_db_recode(self):
        self.add_db_recode_quotation_base()
        self.add_db_recode_detail()
    
    # DB追加：見積基本情報レコード
    def add_db_recode_quotation_base(self):
        # 1. 見積基本情報をDBに登録（新規ならINSERTされ、quotation_idが自動採番される）
        DatabaseController.table_edit(app_data.quotation_base_data)
        
    # DB追加：明細情報レコード
    def add_db_recode_detail(self):
        # 2. 採番されたquotation_idを取得
        new_quotation_id = app_data.quotation_base_data.quotation_id

        # 3. 明細一覧の各データにFKとしてquotation_idをセットしてから、DBに登録する
        for detail_data in app_data.quotation_detail_data_list:
            detail_data.quotation_id = new_quotation_id  # FK設定
            
            # detail_data.tax_rate = app_data.settings_data.tax_rate #明細情報に税率を追加して設定しているので、ここで再設定は不要
            
            DatabaseController.table_edit(detail_data)   # DBへ登録