import tkinter as tk
from app_data_manager import AppDataManager as app_data
from GUI.component_style import ComponentStyle

# SVG画像を入れるか検討中（もうPNGでよくない？）
class SceneMain(tk.Frame):
    def __init__(self, parent,):
        super().__init__(parent)
        
        self._setting_root_frame()
        
        self._create_top_area()
        self._create_bot_area()
        
    def _setting_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def _create_top_area(self):
        # 上部エリアの親フレーム
        top_frame = tk.Frame(self)#, bg="red")
        top_frame.configure(bg="#ffffff")
        top_frame.grid(row=0, column=0, sticky="nsew")
        
        # 中央寄せにするための子フレーム
        inner_frame = tk.Frame(top_frame)
        inner_frame.configure(bg="#ffffff")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # メインタイトルラベル
        main_title_label = tk.Label(inner_frame)
        main_title_label.configure(text="見積作成ツール")
        ComponentStyle.style_label_main_title(main_title_label)
        main_title_label.pack()#(anchor='center', expand=True)
        
        # サブタイトルラベル
        sub_title_label = tk.Label(inner_frame)
        sub_title_label.configure(text="Quotation Manager")
        ComponentStyle.style_label_sub_title(sub_title_label)
        sub_title_label.pack(pady=(4, 0))
        
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def _create_bot_area(self):
        # 下部エリア用Frame作成
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg="#f5f5f5")
        bottom_frame.grid(row=1, column=0, sticky="nsew")

        # 中心に寄せる用Frame作成
        inner_frame = tk.Frame(bottom_frame)
        inner_frame.configure(bg="#f5f5f5")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # メニューボタン作成
        button_info = [
            ("新規見積作成", self._on_create_quote),
            ("履歴一覧", self._on_show_history),
            ("設定", self._on_show_settings),
        ]
        
        for text, cmd in button_info:
            btn = tk.Button(inner_frame)
            btn.configure(text=text, command=cmd)
            ComponentStyle.style_button_main_manue(btn)
            btn.pack(side="left", padx=10)  # ★ side="left" で横並びにする
    
    
    # シーン変更：見積作成シーン
    def _on_create_quote(self):
        app_data.edit_mode_flg = False
        self.master.show_frame("SceneBasicQuoteInformation")
        
    # シーン変更：履歴一覧
    def _on_show_history(self):
        self.master.show_frame("SceneHistoryList")
        
    # シーン変更：設定シーン
    def _on_show_settings(self):
        self.master.show_frame("SceneSetting")
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        app_data.reset_temporary_data()