# このファイルのみで実行可能
import tkinter as tk
from tkinter import ttk

class CompNewSystem():
    def __init__(self):
        self.create_root()
        self.create_base_frame()
        
        self.frame_list = []
        
    
    
    def create_root(self):
        self.root = tk.Tk()
        self.root.title("新構成テスト")
        self.root.geometry("900x600")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_base_frame(self):
        self.base_frame = tk.Frame(self.root)
        self.base_frame.grid_rowconfigure(0, weight=1)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid(row=0, column=0, sticky="nsew")

    def create_frame(self,bg_color):
        frame = tk.Frame(self.base_frame, bg=bg_color, relief="ridge", bd=1)
        frame.pack(fill="x", padx=10, pady=5)
        self.frame_list.append(frame)
        
        
    # 子ウィジェット追加関数を作成し、mainで追加テスト
    def create_label(self, label_name, frame_index):
        lbl = tk.Label(self.frame_list[ frame_index ], text=label_name, bg="whitesmoke")
        lbl.pack(side="left", padx=10, pady=8)


    def main(self):
        self.create_frame("red")
        self.create_label("TOP_A",0)
        self.create_label("TOP_B",0)
        
        self.create_frame("blue")
        self.create_label("TOP_A",1)
        
        self.root.mainloop()
        
app = CompNewSystem()
app.main()

