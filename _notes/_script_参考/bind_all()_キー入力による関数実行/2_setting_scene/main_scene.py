import tkinter as tk

class MainScene(tk.Frame):
    def __init__(self, parent,):
        super().__init__(parent)
        
        self.setting_root_frame()
        self.create_frame1()
        self.create_frame2()
        self.create_buttons_frame()
        self.create_label1()
        
        self.create_button1()
        self.create_button2()
        self.create_button3()
        
        self.layout()
        
    def setting_root_frame(self):
        self.configure(bg="green")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def create_frame1(self):
        self.frame1 = tk.Frame(self, bg="red")
        
    def create_frame2(self):
        self.frame2 = tk.Frame(self, bg="blue")

        # ★ Frame2 の中の縦（row=0）を1等分（中央寄せ用）
        self.frame2.grid_rowconfigure(0, weight=1)

        # ★ Frame2 の中の横（column=0, 1, 2）を均等（1:1:1）に3等分
        for col in range(3):
            self.frame2.grid_columnconfigure(col, weight=1)
            
    # ボタン3つをひとまとめにするための「子フレーム」を作成
    def create_buttons_frame(self): 
        # 背景色をFrame2と同じ blue にして透明に見せる
        self.buttons_frame = tk.Frame(self.frame2, bg="blue")
        
    def create_label1(self):
        self.label1 = tk.Label(self.frame1, text="Frame 1", font=('Helvetica', '35'))
        
    def create_button1(self):
        self.button1 = tk.Button(self.buttons_frame, text='button1', font=('Helvetica', '25'), command=lambda: print("button1が押された"))
        # self.button1.grid(row=0, column=0)
        
    def create_button2(self):
        self.button2 = tk.Button(self.buttons_frame, text='button2', font=('Helvetica', '25'), command=lambda: print("button2が押された"))
        # self.button2.grid(row=0, column=1)
            
    def create_button3(self):
        self.button3 = tk.Button(self.buttons_frame, text='設定', font=('Helvetica', '25'), command=lambda: self.change_scene_setting())
        # self.button3.grid(row=0, column=2)
        
    def layout(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.label1.pack(anchor='center', expand=True)
        
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.buttons_frame.pack(expand=True)# 子フレーム自体を Frame2 の中央に配置する（expand=True で画面中央へ）
        self.button1.pack(side="left", padx=15)
        self.button2.pack(side="left", padx=15)
        self.button3.pack(side="left", padx=15)
        
    # シーン変更：設定シーン
    def change_scene_setting(self):
        self.master.show_frame("SettingScene")
    
        
    def main(self):
        self.root.mainloop()
        
# obj = MainScene()
# obj.main()