# このファイルのみで実行可能
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("コンボボックスの基本")

combo = ttk.Combobox(root, values=["選択肢1", "選択肢2", "選択肢3"])
combo.pack(pady=10)

root.mainloop()