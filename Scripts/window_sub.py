import tkinter as tk
from app_data_manager import AppDataManager as app_data

class WindowSub(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_toplevel()
        
    def init_toplevel(self):
        # self.geometry('450x300') # Frame設定時に決める
        # self.title('設定') # Frame設定時に決める
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 親子関係を設定（Tkの子にする）
        self.transient(self.master)
        
        #【最重要】×ボタンが押されたら、閉じるのではなく「隠す」関数を実行させる
        self.protocol("WM_DELETE_WINDOW", self.on_close_by_x_button)
    
    # 非表示状態にする
    def hidden_window(self):
        # ※既知のバグにより再表示できなくならないようにするため、以下のような処理となっている
        self.attributes("-alpha", 0)  # 透明にする
        self.deiconify()              # 表示状態にする(透明なので見えない)
        self.update()                 # 実際に描画処理を走らせる
        self.withdraw()               # タスクバー等からも隠す
        self.attributes("-alpha", 1)  # 透過度を元に戻しておく(次回表示時のため)
        
        
    # 画面中央に配置する
    def center_window(self):
        
        # メインとサブの最新のサイズ・位置が確定するのを待つ
        self.master.update_idletasks()
        self.update_idletasks()
        
        # メインウィンドウの「幅、高さ、X座標、Y座標」を取得
        main_w = self.master.winfo_width()
        main_h = self.master.winfo_height()
        main_x = self.master.winfo_rootx()
        main_y = self.master.winfo_rooty()
        print(f"[DEBUG] main: {main_w}x{main_h} at ({main_x},{main_y})")  # ★追加
        
        # サブウィンドウの現在の「幅、高さ」を取得
        sub_w = self.winfo_width()
        sub_h = self.winfo_height()
        print(f"[DEBUG] sub: {sub_w}x{sub_h}")  # ★追加
        
        # メインウィンドウの中心に合わせるための座標を計算
        x = main_x + (main_w - sub_w) // 2
        y = main_y + (main_h - sub_h) // 2
        
        # 計算した座標をサブウィンドウに適用して移動させる
        self.geometry(f"+{x}+{y}")
            
            
    # 表示/非表示切り替え
    def toggle_state(self):
        if self.wm_state() == "normal":
            # self.state("withdraw")
            self.grab_release()  # 操作制限を解除
            self.withdraw() # 非表示にする
        else:
            # self.state("normal")
            # self.deiconify() # normal（表示状態）に戻す
            self.attributes("-alpha", 0)
            self.center_window()
            self.deiconify() # normal（表示状態）に戻す
            self.update_idletasks()
            self.attributes("-alpha", 1)
        
            # self.lift()
            self.grab_set()       # ★ここでメインウィンドウの操作を止める
            self.focus_set()      # サブウィンドウにフォーカスを移す
            
    # 外部から、画面を設定する
    def set_scene_frame(self, flame : tk.Frame, title : str, size : str):
        self.frame = flame
        self.title(title)
        self.geometry(size)
        
        self.hidden_window()
        
        # self.update_idletasks() # Frameのサイズに合わせるために入れていたが、機能していないっぽい
        # self.geometry("")  # 明示指定を解除し、内容(Frame)に合わせて自動サイズ調整させる
        # self.hidden_window() # 無くても変わらなそう
        
    # 追加：×ボタン専用の処理
    def on_close_by_x_button(self):
        print("×が押されました")
        app_data.decide_result.set(False)  # ★これが無いと、wait_variableが永遠に解放されない
        self.toggle_state()
            
            
            
            