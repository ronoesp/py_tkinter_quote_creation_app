import tkinter as tk
from .component_style import ComponentStyle

# ==========================================
# TOPエリア（画面タイトル）
# ==========================================
class ComponentAreaTop(tk.Frame):
    def __init__(self, parent, title : str):
        super().__init__(parent)
        self._init_frame()
        self._create_label_title(title)
        
    def _init_frame(self):
        self.configure(bg="#333333", height=50)
        self.pack(side="top", fill="x") # 上部に固定して、横幅いっぱいに広げる (fill="x")
        
    def _create_label_title(self, title):
        self.title_label = tk.Label(self) # ウィジェット作成
        self.title_label.configure(text=title)
        self.title_label.pack(pady=10) # 並べる
        
        ComponentStyle.style_label_title(self.title_label)