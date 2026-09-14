import tkinter as tk
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from app_data_manager import AppDataManager as app_data
from GUI.tkinter_support import TkinterSupport

# ※サブウィンドウ上に表示する
class SceneCheck(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.init_root_frame()
        
        self.create_top_area()
        self.create_bot_area()
        self.create_mid_area()
        
    def init_root_frame(self):
        # self.configure(width=900, height=300)   # ★サイズ指定
        # self.grid_propagate(False)              # ★中身に合わせて縮まないようにする
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        title = "確認画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self, show_msg_box=False)
        
        text = " いいえ "
        self.bot_area.create_button(text, self.cancel)
        
        text = "  はい  "
        self.bot_area.create_button(text, self.decide)
        
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
        self.set_text()
        
    def set_text(self):
        text = ("本当に実行しますか？")
        TkinterSupport.set_text_adjust(text, self.text)
    
    def decide(self):
        print("はい")
        app_data.decide_result.set(True)   # ★これで待機が解除される
        self.master.toggle_state()
        
    def cancel(self):
        print("いいえ")
        app_data.decide_result.set(False)   # ★これで待機が解除される
        self.master.toggle_state()
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    # ※サブディスプレイで使用するものには必要ない（今のところ）
    # def init_active(self):
    #     pass
        