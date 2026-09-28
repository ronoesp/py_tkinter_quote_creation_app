import tkinter as tk
from tkinter import ttk

# このファイルのみで実行可能
class SceneSort(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_notebook()
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # タブごとに中身となるFrameを用意する
        self.tab_name = tk.Frame(self.notebook)
        self.tab_date = tk.Frame(self.notebook)
        self.tab_price = tk.Frame(self.notebook)
        
        # タブとして登録(表示名を指定)
        self.notebook.add(self.tab_name, text="名前順")
        self.notebook.add(self.tab_date, text="日付順")
        self.notebook.add(self.tab_price, text="金額順")
        
        # タブが切り替わったときのイベントを拾いたい場合
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def on_tab_changed(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        print(f"選択されたタブ: {selected_tab}")
        # ここで並び替えタイプに応じた処理を呼ぶ想定(今回は未実装でOK)
        

root = tk.Tk()
root.title("見積作成ツール")
root.geometry("900x600")

# 画面全体を上下 1:1 に分割
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = SceneSort(root)
frame.grid(row=0, column=0, sticky="nsew")  # ★これが抜けていた

root.mainloop()
