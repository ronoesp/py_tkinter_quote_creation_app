import tkinter as tk

# ==========================================
# ページ切り替えエリア
# ==========================================
class ComponentAreaPageControll(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._init_frame()
        self._create_contents()
        
    def _init_frame(self):
        self.configure(bg="#dddddd", height=40)
        self.pack(side="bottom", fill="x", anchor="center") # 下部に固定して、横幅いっぱいに広げる (fill="x")
        
    def _create_contents(self):
        # 3つのウィジェットをまとめる、内側専用のFrameを作る
        inner_frame = tk.Frame(self, bg="#dddddd")
        inner_frame.pack(expand=True)  # 中央に配置される
    
        # 左ボタン
        self.left_button = tk.Button(inner_frame)
        self.left_button.configure(text="<")
        self._pack_common_style(self.left_button)
        # self.left_button.pack(side="left", padx=15, pady=8)
        
        # 中央ラベル：ページ表示
        self.center_label = tk.Label(inner_frame)
        self.center_label.configure(text="/", bg="whitesmoke")
        self._pack_common_style(self.center_label)
        # self.center_label.pack(side="left", padx=15, pady=8)

        # 右ボタン
        self.right_button = tk.Button(inner_frame)
        self.right_button.configure(text=">")
        self._pack_common_style(self.right_button)
        # self.right_button.pack(side="left", padx=15, pady=8)
        
    def _pack_common_style(self, component):
        component.pack(side="left", padx=15, pady=8)
        
    def set_cmd_button(self,left_cmd, right_cmd):
        self.left_button.configure(command=lambda: left_cmd())
        self.right_button.configure(command=lambda: right_cmd())
        
    def update_center_text(self, c_text: str):
        self.center_label.configure(text=c_text)