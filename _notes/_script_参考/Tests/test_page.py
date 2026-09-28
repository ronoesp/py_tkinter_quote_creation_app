import tkinter as tk


class PageNavigator(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_nav_widgets()
    
    def create_nav_widgets(self):
        
        frame_top = tk.Frame(self)
        frame_top.pack(expand=True)
        self.page_label_top = tk.Label(frame_top, text="TOP", font=("Meiryo", 12), width=10)
        self.page_label_top.pack()
        
        
        
        # 3つのウィジェットをまとめる内側のコンテナ
        nav_container = tk.Frame(self)
        nav_container.pack(expand=True)  # ★これだけで親(self)の中央に配置される
        
        # 戻るボタン
        self.btn_prev = tk.Button(nav_container, text="＜ 戻る", width=8, command=self.on_prev)
        self.btn_prev.pack(side="left", padx=10)
        
        # 現在のページを表すテキスト
        self.page_label = tk.Label(nav_container, text="1 / 10", font=("Meiryo", 12), width=10)
        self.page_label.pack(side="left", padx=10)
        
        # 進むボタン
        self.btn_next = tk.Button(nav_container, text="進む ＞", width=8, command=self.on_next)
        self.btn_next.pack(side="left", padx=10)
        
        
        
        frame_bot = tk.Frame(self)
        frame_bot.pack(expand=True)
        self.page_label_bot = tk.Label(frame_bot, text="BOT", font=("Meiryo", 12), width=10)
        self.page_label_bot.pack()
    
    def on_prev(self):
        print("戻るボタンが押されました(処理は未実装)")
    
    def on_next(self):
        print("進むボタンが押されました(処理は未実装)")


# ---- 単体動作確認用 ----
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ページナビゲーション テスト")
    root.geometry("600x400")
    
    nav = PageNavigator(root)
    nav.pack(fill="both", expand=True)  # 親いっぱいに広げる(中央配置の土台を作る)
    
    root.mainloop()