import tkinter as tk
from .component_style import ComponentStyle

# ==========================================
# BOTTOMエリア（フッター・ボタン等）
# ==========================================
class ComponentAreaBot(tk.Frame):
    def __init__(self, parent, show_msg_box: bool = True):
        super().__init__(parent)
        self._init_frame()
        self._create_msg_box(show_msg_box)
        
    def _init_frame(self):
        self.configure(bg="#dddddd", height=110)
        self.pack(side="bottom", fill="x") # 下部に固定して、横幅いっぱいに広げる (fill="x")
        self.pack_propagate(False) # 幅が一定に保たれる（ウィジェットの最大幅で修正されない）
    
    def _create_msg_box(self,show_msg_box):
        self.label_msg_box = tk.Label(self)
        ComponentStyle.style_label_msg_box(self.label_msg_box)
        if show_msg_box:
            self.show_msg_box()
        else:
            self.hide_msg_box()
        
    def create_button(self, b_text, cmd):        
        button = tk.Button(self)
        button.pack(side="right", padx=10, pady=5)
        ComponentStyle.style_button(button)
        button.configure(text=b_text, command=lambda: cmd())
        
        return button
        
    def update_msg_box(self, b_text):
        self.label_msg_box.configure(text=b_text)
        
    def hide_msg_box(self):
        self.label_msg_box.pack_forget()

    def show_msg_box(self):
        self.label_msg_box.pack(side="left", padx=15, pady=8)  # 再度配置し直す