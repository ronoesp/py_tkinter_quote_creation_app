import tkinter as tk

# ※現在は設定項目が少ない（デザイン決まってない）ので一旦保留しておく
class AtomicPYButton(tk.Button):
    def __init__(self, parrent):
        super.__init__(parrent)
        self.create_size_pattern()
        self.setting_base()
    
    # ボタンサイズタイプ
    def create_size_pattern(self):
        self.size_wh_type1 = [5,5]
        self.size_wh_type2 = [10,5]
        self.size_wh_type3 = [15,5]
        self.size_wh_type4 = [15,10]
    
    def setting_base(self):
        self.configure(font=('Helvetica', '25'))
        
    def set_text(self, b_text):
        self.configure(text=b_text)
    
    def set_size_type(self, size_type):
        self.configure(width=size_type[0], height=size_type[1])
    
    def set_command(self, b_command):
        self.configure(command=b_command)
        
        
    