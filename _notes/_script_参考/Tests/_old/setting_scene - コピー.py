import tkinter as tk

# Frameを上下に６つ作成（レイアウト通りにする）
class SettingScene(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setting_root_frame()
        
        self.create_frame1()
        self.create_frame2()
        self.create_frame3()
        self.create_frame4()
        self.create_frame5()
        self.create_frame6()
        
        self.create_label1()
        self.create_label2()
        self.create_label3()
        self.create_label4()
        self.create_label5()
        self.create_label_err()
        
        self.create_entry1()
        self.create_entry2()
        self.create_entry3()
        self.create_entry4()
        
        self.create_button1()
        self.create_button2()
        
        # self.create_buttons_frame()
        # self.create_label1()
        
        # self.create_button1()
        # self.create_button2()
        # self.create_button3()
        
        self.layout()
        
        
    
    # ※ここも６分割に対応する必要がある？
    def setting_root_frame(self):
        # self.configure(bg="green")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
        
    def create_frame1(self):
        self.frame1 = tk.Frame(self, bg="red")
        
    def create_frame2(self):
        self.frame2 = tk.Frame(self, bg="blue")
            
    def create_frame3(self):
        self.frame3 = tk.Frame(self, bg="red")  
    
    def create_frame4(self):
        self.frame4 = tk.Frame(self, bg="blue")
        
    def create_frame5(self):
        self.frame5 = tk.Frame(self, bg="red")  
        
    def create_frame6(self):
        self.frame6 = tk.Frame(self, bg="blue")
            
            
            
            
    def create_label1(self):
        self.label1 = tk.Label(self.frame1, text="設定画面", font=('Helvetica', '15'), anchor='center', width=11)
        
    def create_label2(self):
        self.label2 = tk.Label(self.frame2, text="消費税率", font=('Helvetica', '15'), anchor='center', width=11)
            
    def create_label3(self):
        self.label3 = tk.Label(self.frame3, text="自社名", font=('Helvetica', '15'), anchor='center', width=11)
        
    def create_label4(self):
        self.label4 = tk.Label(self.frame4, text="自社住所", font=('Helvetica', '15'), anchor='center', width=11)
        
    def create_label5(self):
        self.label5 = tk.Label(self.frame5, text="自社電話番号", font=('Helvetica', '15'), anchor='center', width=11)
                 
    def create_label_err(self):
        self.label_err = tk.Label(self.frame6, text="エラー情報", font=('Helvetica', '15'), anchor='center', width=11)
    
    
    def create_entry1(self):
        self.entry1 = tk.Entry(self.frame2,font=("Helvetica", 14), justify="left", width=20)
        
    def create_entry2(self):
        self.entry2 = tk.Entry(self.frame3,font=("Helvetica", 14), justify="left", width=20)
            
    def create_entry3(self):
        self.entry3 = tk.Entry(self.frame4,font=("Helvetica", 14), justify="left", width=20)
            
    def create_entry4(self):
        self.entry4 = tk.Entry(self.frame5,font=("Helvetica", 14), justify="left", width=20)
        
        
    def create_button1(self):
        self.button1 = tk.Button(self.frame6, text='戻る', font=('Helvetica', 14), command=lambda: self.change_scene_main())
    
    def create_button2(self):
        self.button2 = tk.Button(self.frame6, text='保存', font=('Helvetica', 14), command=lambda: print("設定を保存しました"))
     
        
    def layout(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame3.grid(row=2, column=0, sticky="nsew")
        self.frame4.grid(row=3, column=0, sticky="nsew")
        self.frame5.grid(row=4, column=0, sticky="nsew")
        self.frame6.grid(row=5, column=0, sticky="nsew")
        
        self.label1.pack(side="left", padx=15, anchor='center', expand=True)
        self.label2.pack(side="left", padx=15, anchor='w')
        self.label3.pack(side="left", padx=15, anchor='w')
        self.label4.pack(side="left", padx=15, anchor='w')
        self.label5.pack(side="left", padx=15, anchor='w')
        self.label_err.pack(side="left", padx=15, anchor='w')
                
        self.entry1.pack(side="left", padx=15, anchor='w')
        self.entry2.pack(side="left", padx=15, anchor='w')
        self.entry3.pack(side="left", padx=15, anchor='w')
        self.entry4.pack(side="left", padx=15, anchor='w')
        
        self.button1.pack(side="right", padx=15, anchor='e')
        self.button2.pack(side="right", padx=15, anchor='e')

    
    # シーン変更：設定シーン
    def change_scene_main(self):
        self.master.show_frame("MainScene")
        print("メイン画面に戻ります")
        
    def main(self):
        self.root.mainloop()