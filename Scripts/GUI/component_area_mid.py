import tkinter as tk
import tkinter as ttk
from .component_style import ComponentStyle
from calender.date_picker_entry import DatePickerEntry


# =======================
# ■残りの作業
# ・Entryに、空欄なら色を付ける付けない設定をできるようにする
# ・カレンダーまわりの構成見直し
# =======================

# ==========================================
# Middleエリア（スクロール可能なCanvas領域）
# ==========================================
class ComponentAreaMid(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._scrollable_frame_base_setting()
        self.frame_list = []
        
    # ==========================================
    # ベースとなるスクロール可能なFrame領域を作成
    # ==========================================
    def _scrollable_frame_base_setting(self):
        
        # ウィジェット作成
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollable_frame = ttk.Frame(self.canvas) # scrollable_frame の中身は .grid() や .pack() を自由に使用できる
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame)
        
        # 設定
        self.canvas.configure(yscrollcommand=self.scrollbar.set,  highlightthickness=0)
        self.scrollbar.configure(orient="vertical", command=self.canvas.yview)
        self.canvas.itemconfigure(self.canvas_window, anchor="nw")
        
        # スクロール範囲の自動設定 ＆ Canvasの幅変更に内部Frameを追従させる
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # 並べる
        self.pack(side="top", fill="both", expand=True)# expand=True と fill="both" で余った中央部分をすべて占有
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    # 中身のサイズに合わせてスクロール範囲を自動アップデート
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    # 横幅をCanvasの幅にフィットさせる
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
        
    
    # ==========================================
    # ウィジェット作成（アトミックデザイン）
    # ==========================================
    # 新構成：間隔開ける用のFrame（リストに入れない）
    def create_empty_area(self, l_height : float):
        frame = tk.Frame(self.scrollable_frame)
        frame.configure(height=l_height, padx=10, pady=5)
        frame.pack(fill="x")
        return frame

    # 新構成：Frame
    def create_frame(self):
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(fill="x")
        self.frame_list.append(frame)
        return frame
        
    def create_frame_ridge(self):
        frame = self.create_frame()
        ComponentStyle.style_frame_ridge(frame)
        return frame    
    
    # 新構成：Label
    def create_label(self, label_name, l_side = "top"):
        last_frame = self.frame_list[-1]
        lbl = tk.Label(last_frame)
        lbl.configure(text=label_name, bg="whitesmoke", padx=10, pady=8)
        lbl.pack(side=l_side)
        return lbl
        
    # 新構成：Entry
    def create_entry(self, l_side = "top"):
        last_frame = self.frame_list[-1]
        ent = tk.Entry(last_frame)
        ent.configure(bg="white", width=15)
        ent.pack(side=l_side, padx=10) # Entryのconfigureにはpadxはない（ウィジェットによって異なる）
        return ent
    

    # ※ここの仕様は後で考える：Entryではなくカレンダーウィジェットを直接受け取るようにしたい
    # 　→その後、カレンダークラスの関数経由でEntryウィジェットを取得する
    # 新個性：DateEntryをToplevelウィジェット経由で使用（Frameウィジェットを継承したクラス）
    def create_date_picker_entry_frame(self, l_side = "top", required=False):
        last_frame = self.frame_list[-1]
        # frame = DatePickerEntryFrame(last_frame, date_pattern="yyyy/mm/dd", required=required)
        frame = DatePickerEntry(last_frame, required=required)
        frame.pack(side=l_side, padx=10)
        return frame
    
    
    # 新構成：Button
    def create_button(self, b_text, cmd, l_side = "top"):
        last_frame = self.frame_list[-1]
        btn = tk.Button(last_frame)
        btn.configure(text=b_text, command=lambda: cmd())
        btn.pack(side=l_side, padx=10, pady=5)
        ComponentStyle.style_button(btn)
        return btn
        
    # 新構成：Text
    def create_text_normal(self, l_side = "top"):
        last_frame = self.frame_list[-1]
        txt = tk.Text(last_frame)
        txt.pack(side=l_side)
        ComponentStyle.style_text_normal(txt)
        return txt
        
    def create_text_dark(self, l_side = "top"):
        last_frame = self.frame_list[-1]
        txt = tk.Text(last_frame)
        txt.pack(side=l_side, expand=True, fill=tk.NONE)
        ComponentStyle.style_text_dark(txt)
        return txt