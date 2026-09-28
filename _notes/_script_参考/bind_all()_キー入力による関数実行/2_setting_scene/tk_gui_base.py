import tkinter as tk

# 参考：https://tech-lab.sios.jp/archives/38432
class TKGUIBase(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setting_root()

        # フレームコンテナ作成
        self.create_frame_container()
        
        # フレームコンテナを各フレームの親にする
        self.create_frames()

        # 一番最初に表示するフレームの指定
        self.show_frame("MainScene")  

        # フレーム切り替えの方法を設定
        self.set_frame_change_event()
        
    def setting_root(self):
        self.title("見積作成ツール")
        self.geometry("900x600")

        # 画面全体を上下 1:1 に分割
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        
    # 作成するフレームの格納先を用意する
    def create_frame_container(self):
        self.frames = {}
            
    # フレームのインスタンス作成＆格納＆フレームコンテナを親にする
    def create_frames(self):
        from main_scene import MainScene
        from setting_scene import SettingScene
        
        self.frame_class_list = [MainScene, SettingScene]
        for F in self.frame_class_list:
            frame = F(self)
            self.frames[F.__name__] = frame

    # フレームを切り替える（画面の一番上に移動する）
    def show_frame(self, _frame):
        frame: tk.Frame = self.frames[_frame]
        # フレームにフォーカスを当てる
        frame.focus_force()
        # フレームを前面に配置
        frame.tkraise()
        
    # フレーム切り替えの方法を設定：キーボードの数字入力で切り替えるように設定
    def set_frame_change_event(self):
        # bind_all:キーボードやマウスイベントを適用するメソッド
        # 関数のデフォルト引数（frame_class=F の部分）は、lambda が作成されたその瞬間に値が評価されて保存されるという特別な性質を持っています。
        # 1回目のループ：frame_class = FrameOne という値が保存された関数ができる
        # 2回目のループ：frame_class = FrameTwo という値が保存された関数ができる
        # 3回目のループ：frame_class = FrameThree という値が保存された関数ができる
        # このようにして、ループが回るたびに「その時点での F の値」をコピーして関数内に閉じ込めることができるため、期待通りに動くようになります。
        for idx, F in enumerate(self.frame_class_list, start=1):
            self.bind_all(str(idx), lambda e, frame_class=F: self.show_frame(frame_class.__name__))
            
    def main(self):
        self.mainloop()