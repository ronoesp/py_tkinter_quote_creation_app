import tkinter as tk
# from functools import partial
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from app_data_manager import AppDataManager as app_data
from GUI.tkinter_support import TkinterSupport
from quotation_csv_exporter import QuotationCsvExporter as csv_output

class SceneComplete(tk.Frame):
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
        title = "完了画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)
        
        # メイン画面に戻る
        text = " 終了 "
        self.bot_area.create_button(text, self.return_scene)
        
        text = " 出力 "
        self.bot_area.create_button(text, self.output)
        
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
    
    def set_text(self):        
        # 文章作成
        number_str = str(app_data.quotation_base_data.quotation_number)
        mode = "編集" if app_data.edit_mode_flg else "作成"
        text = ("見積書の" + mode + "が完了しました。\n"
                "見積番号：" + number_str)
        TkinterSupport.set_text_adjust(text, self.text)
        
    def return_scene(self):
        self.master.show_frame("SceneMain")
        print("メイン画面に戻ります")
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        self.bot_area.update_msg_box("出力ボタンからCSVファイルを出力できます。\n終了ボタンからメイン画面に戻ります。")
        self.set_text()
        
    # CSVファイルを出力する
    def output(self):
        if csv_output.export():
            self.bot_area.update_msg_box("CSVファイルを出力しました。")