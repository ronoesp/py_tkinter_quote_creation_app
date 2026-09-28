import tkinter as tk
from tkinter import ttk

class TKScrollbarTest():
    def __init__(self):
        self.create_root()
        self.create_top_area()
        self.create_bottom_area()
        self.create_center_area()
        self.populate_center_content()
        
        self.root.mainloop()

    def create_root(self):
        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.minsize(width=350, height=300)

    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        self.top_frame = tk.Frame(self.root, bg="#333333", height=50)
        # 上部に固定して、横幅いっぱいに広げる (fill="x")
        self.top_frame.pack(side="top", fill="x")
        
        self.title_label = tk.Label(
            self.top_frame, 
            text="画面タイトル (TOP)", 
            fg="white", 
            bg="#333333", 
            font=("Arial", 14, "bold")
        )
        self.title_label.pack(pady=10)

    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bottom_area(self):
        self.bottom_frame = tk.Frame(self.root, bg="#dddddd", height=40)
        # 下部に固定して、横幅いっぱいに広げる (fill="x")
        self.bottom_frame.pack(side="bottom", fill="x")
        
        self.bottom_label = tk.Label(
            self.bottom_frame, 
            text="フッター領域 (BOTTOM)", 
            bg="#dddddd"
        )
        self.bottom_label.pack(pady=8)

    # ==========================================
    # 3. CENTERエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_center_area(self):
        # TOPとBOTTOMの間（残りの空間）を埋める親Frame
        self.center_container = tk.Frame(self.root)
        # expand=True と fill="both" で余った中央部分をすべて占有
        self.center_container.pack(side="top", fill="both", expand=True)

        # CanvasとScrollbarを構築
        self.canvas = tk.Canvas(self.center_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.center_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Canvas内に描画・スクロールさせる内部Frameの作成
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # スクロール範囲の自動設定 ＆ Canvasの幅変更に内部Frameを追従させる
        self.scrollable_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>", 
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

    # ==========================================
    # 4. CENTER内部へのコンテンツ追加（テスト用）
    # ==========================================
    def populate_center_content(self):
        # scrollable_frame の中身は .grid() や .pack() を自由に使用できます
        for i in range(2):
            frame = tk.Frame(self.scrollable_frame, bg="whitesmoke", relief="ridge", bd=1)
            frame.pack(fill="x", padx=10, pady=5)
            
            lbl = tk.Label(frame, text=f"コンテンツ項目 {i+1}", bg="whitesmoke")
            lbl.pack(side="left", padx=10, pady=8)
            
            btn = ttk.Button(frame, text="詳細")
            btn.pack(side="right", padx=10)

if __name__ == "__main__":
    app = TKScrollbarTest()