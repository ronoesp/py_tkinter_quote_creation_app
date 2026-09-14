import tkinter as tk
from tkinter import ttk
from window_sub import WindowSub as window_sub
from app_data_manager import AppDataManager as app_data

# 参考：https://tech-lab.sios.jp/archives/38432
class WindowMain(tk.Tk):
    def __init__(self):
        super().__init__()
        
        style = ttk.Style()
        style.theme_use('clam')  # ← ここで最初に設定する
        
        self.setting_root()
        
        # アプリの一時データ保存用クラスの初期化
        app_data.init(self)


        # サブウィンドウ作成（確認用ウィンドウ）
        self.create_check_window()
        
        # ■開始時に別画面が表示される問題対策：まずウィンドウ自体を非表示にする
        #  →これを実行するとサブウィンドウが表示されなくなるため使用しない方向に決定
        # self.withdraw()  
        

        
        
        # フレームのクラスリストを作成
        self.create_frame_class_list()
        
        # 各フレーム（画面）を作成＆格納
        self.create_frames()

        # 一番最初に表示する画面の指定
        self.show_frame("SceneMain")  
        
        
        # ■開始時に別画面が表示される問題対策：準備が整ってから、初めてウィンドウを表示する
        # 　→withdraw() を使用しないのでこれも不要
        # self.deiconify()  

        
    def setting_root(self):
        self.title("見積作成ツール")
        self.geometry("900x600")

        # 画面全体を上下 1:1 に分割
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
    # 作成するフレームのクラスリストを用意する
    def create_frame_class_list(self):
        from Scenes.scene_main import SceneMain
        from Scenes.scene_setting import SceneSetting
        from Scenes.scene_basic_quote_information import SceneBasicQuoteInformation
        from Scenes.scene_detail_information import SceneDetailInformation
        from Scenes.scene_preview import ScenePreview
        from Scenes.scene_complete import SceneComplete
        from Scenes.scene_show_history import SceneShowHistory
        from Scenes.scene_complete_delete_history import SceneCompleteDeleteHistory
        from Scenes.scene_history_list import SceneHistoryList
        
        self.frame_class_list = [SceneMain, 
                                 SceneSetting, 
                                 SceneBasicQuoteInformation, 
                                 SceneDetailInformation, 
                                 ScenePreview,
                                 SceneComplete,
                                 SceneShowHistory,
                                 SceneCompleteDeleteHistory,
                                 SceneHistoryList]


    # フレームのインスタンス作成＆格納＆このクラス(root)を親にする
    def create_frames(self):
        self.frames = {}
        
        for F in self.frame_class_list:
            frame = F(self)
            self.frames[F.__name__] = frame
            
            # アプリ開始時の見た目問題、サブウィンドウの表示問題を解決するために以下を追加
            frame.lower()  # ★作った直後に、すぐ一番奥に沈めてしまう


    # フレームを切り替える（画面の一番上に移動する）
    def show_frame(self, scene_class_name):
        # 画面を構成するクラス名から辞書検索してフレーム（クラスのインスタンス）を取得する
        frame: tk.Frame = self.frames[scene_class_name]
        # フレームにフォーカスを当てる
        frame.focus_force()
        # フレームを前面に配置
        frame.tkraise()
        
        # ※フレームを切り替えた際に実行する共通関数を作成する（設定データから文章の更新などを行う）
        frame.init_active()
        
        
    # サブウィンドウ作成（確認用ウィンドウ）
    def create_check_window(self):
        self.window_sub = window_sub(self)
        
        from Scenes.scene_check import SceneCheck
        self.window_sub.set_scene_frame( SceneCheck(self.window_sub), "最終確認", "500x300")
        self.window_sub.update()     # サイズ確定を待つ
        self.window_sub.center_window()
        
    
    def change_sub_window_state(self):
         self.window_sub.toggle_state()
        

    def main(self):
        self.mainloop()