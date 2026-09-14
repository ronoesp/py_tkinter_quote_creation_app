import tkinter as tk
# from functools import partial
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from app_data_manager import AppDataManager as app_data
from create_quotation_document import CreateQuotationDocument as quote_text
from DB.data_base_controller import DatabaseController as db_ctr
from GUI.tkinter_support import TkinterSupport
from quotation_csv_exporter import QuotationCsvExporter as csv_output

class SceneShowHistory(tk.Frame):
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
        title = "履歴確認画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)
        
        text = " 戻る "
        self.bot_area.create_button(text, self.return_scene)
        
        text = " 出力 "
        self.bot_area.create_button(text, self.output)
        
        text = " 削除 "
        self.bot_area.create_button(text, self.delete_data)
        
        text = " 編集 "
        self.bot_area.create_button(text, self.edit_data)
        
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
            
    def return_scene(self):
        self.master.show_frame("SceneHistoryList")
        print("履歴画面に戻ります")
    
    # CSVファイルを出力する
    def output(self):
        if csv_output.export():
            self.bot_area.update_msg_box("CSVファイルを出力しました。")
        
    def delete_data(self):
        # 確認画面（サブウィンドウ）を表示する
        self.master.change_sub_window_state()
        self.master.wait_variable(app_data.decide_result)  # ★変数が変化するまでここで待機
        
        # AppDataManagerクラスの変数チェック
        if app_data.decide_result.get() == True:
            # 現在選択中の見積基本情報レコードから見積IDを取得する
            id = app_data.quotation_base_data.quotation_id
            
            # 見積IDを持つ明細情報レコードを削除
            db_ctr.delete_record("quotation_detail", "quotation_id", id)
            
            # 見積IDを持つ見積基本情報レコードを削除
            db_ctr.delete_record("quotation_base", "quotation_id", id)
            
            print("見積データを削除します（未実装）")
            self.master.show_frame("SceneCompleteDeleteHistory")
        else:
            print("いいえが選択されました")
        
        # チェック用変数初期化
        app_data.decide_result.set(False)
        
        
    def edit_data(self):
        app_data.edit_mode_flg = True
        self.master.show_frame("SceneBasicQuoteInformation")
        print("見積書を編集します（未実装）")
        
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        self.set_text()