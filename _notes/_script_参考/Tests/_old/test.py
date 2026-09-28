import tkinter as tk
from tkinter import ttk

# ==========================================
# 共通：スクロール機能付きFrameコンポーネント
# ==========================================
class ScrollablePage(tk.Frame):
    def __init__(self, parent, rows_count=2, row_height=150):
        super().__init__(parent)
        self.rows_count = rows_count
        self.row_height = row_height

        # 1. CanvasとScrollbarの配置
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # 2. Canvas内部のコンテンツ用Frameを作成
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # 3. 行の高さを固定するためのグリッド設定
        for r in range(self.rows_count):
            # minsize を指定することで、中身の行数や要素量に左右されず行高を確保
            self.scrollable_frame.grid_rowconfigure(r, minsize=self.row_height, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # 4. イベントバインド（スクロール領域と横幅の自動調整）
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        # 中身のサイズに合わせてスクロール範囲を自動アップデート
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # 横幅をCanvasの幅にフィットさせる
        self.canvas.itemconfig(self.canvas_window, width=event.width)


# ==========================================
# 各画面の定義
# ==========================================
class Page1(ScrollablePage):
    """行数が少ない画面 (例: 2行)"""
    def __init__(self, parent, controller):
        # 2行、1行あたり150pxで作成
        super().__init__(parent, rows_count=2, row_height=150)

        # 0行目
        cell0 = tk.Label(self.scrollable_frame, text="画面1：行 0 (トップ領域)", bg="lightblue")
        cell0.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 1行目
        cell1 = tk.Frame(self.scrollable_frame, bg="lightyellow")
        cell1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        btn = ttk.Button(cell1, text="画面2へ遷移", command=lambda: controller.show_page("Page2"))
        btn.pack(expand=True)


class Page2(ScrollablePage):
    """行数が多い画面 (例: 6行 -> 画面に入りきらないのでスクロール発生)"""
    def __init__(self, parent, controller):
        # 6行、1行あたり150pxで作成（合計900pxになるためスクロールが発生）
        super().__init__(parent, rows_count=6, row_height=150)

        colors = ["#ffcccc", "#ccffcc", "#ccccff", "#ffffcc", "#ffccff", "#ccffff"]
        for i in range(6):
            cell = tk.Frame(self.scrollable_frame, bg=colors[i])
            cell.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            
            lbl = tk.Label(cell, text=f"画面2：行 {i}", bg=colors[i])
            lbl.pack(side="left", padx=10)
            
            if i == 0:
                btn = ttk.Button(cell, text="画面1へ戻る", command=lambda: controller.show_page("Page1"))
                btn.pack(side="right", padx=10)


# ==========================================
# メインアプリケーション（画面遷移の制御）
# ==========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("画面遷移 & スクロールレイアウト固定")
        self.geometry("500x400")  # 画面の高さは400px

        # 画面切り替え用の親コンテナ
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (Page1, Page2):
            page_name = PageClass.__name__
            # 重ね合わせて配置
            page = PageClass(parent=container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("Page1")

    def show_page(self, page_name):
        """指定した画面を最前面に表示"""
        page = self.pages[page_name]
        page.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()