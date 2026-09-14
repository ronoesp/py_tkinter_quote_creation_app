import tkinter as tk
from functools import partial
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from DB.data_base_controller import DatabaseController
from DB.table_data_model import *
from app_data_manager import  AppDataManager as app_data
from calender.date_picker_entry import DatePickerEntry

class SceneBasicQuoteInformation(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.init_root_frame()
        self.define_field()
        
        self.create_top_area()
        self.create_bot_area()
        self.create_mid_area()
        
        self.bind_required_entry_highlight() # 必須項目を目立たせるように仕込む
        self.setup_valid_until_mindate() # カレンダー選択範囲を仕込む
        self.reset_data()
        
    def init_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        
        title = "見積基本情報画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)
        
        text = " 戻る "
        self.bot_area.create_button(text, self.return_scene)
        
        text = " 次へ "
        # cmd = partial(print, "見積情報画面へ移動します（未実装）")
        self.bot_area.create_button(text, self.next_scene)
        
    # ==========================================
    # 3. Middleエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_mid_area(self):
        self.mid_area = mid_area(self)
        self.entry_list = [] # 各ウィジェットなどのデータを辞書型で作成し、配列に持たせる

        # 先にEntryとカレンダーだけをリストに追加
        for data in self.field_definitions:
            frame = self.mid_area.create_frame_ridge()
            label = self.mid_area.create_label(data["name"], "left")

            # Entry作成orカレンダーFrame作成
            dpe_frame = None
            if data["ent_type"] == "":
                entry = self.mid_area.create_entry("right")
            elif data["ent_type"] == "date_base":
                dpe_frame = self.mid_area.create_date_picker_entry_frame("right", True)
                entry = dpe_frame.get_entry()
            elif data["ent_type"] == "date":
                dpe_frame = self.mid_area.create_date_picker_entry_frame("right")
                entry = dpe_frame.get_entry()
                
            # # 必須項目の仕込み
            # if data["required"] == True:
            #     new_text = data["name"] + "※"
            #     label.configure(text=new_text)
                
            #     # DatePickerEntryFrameクラスは独自にEntryチェック機能をbindするため、ここでは設定しないようにする
            #     if data["ent_type"] == "":
            #         entry.bind("<FocusOut>", self.check_required_entry_and_focus, add="+")
        
            # ※カレンダーのFrameも辞書に追加。date_picker_entry_frame_listは削除して辞書内のものを使用するよう変更予定
            self.entry_list.append({"column" : data["column"], "required" : data["required"], "label" : label, "entry" : entry, "dpe_frame" : dpe_frame})
    
    
    # ==========================================
    # 必須項目を目立たせるように仕込む
    # ==========================================
    def bind_required_entry_highlight(self):
        for data in self.entry_list:
            if data["required"] == True:
                new_text = data["label"].cget("text") + "※"
                data["label"].configure(text=new_text)
                
                # DatePickerEntryFrameクラスは独自にEntryチェック機能をbindするため、ここでは設定しないようにする
                if data["dpe_frame"] == None:
                    data["entry"].bind("<FocusOut>", self.check_required_entry_and_focus, add="+")
    
    
    # ==========================================
    # カレンダー選択範囲を仕込む
    # ==========================================
    def setup_valid_until_mindate(self):
        base_dpe_frame = None
        target_dpe_frame = None
        for data in self.entry_list:
            if data["column"] == "created_date":
                base_dpe_frame = data["dpe_frame"]
            elif data["column"] == "valid_until":
                target_dpe_frame = data["dpe_frame"]
        
        # # 契約期限日を作成日以前に設定できないよう仕込む
        # target_dpe_frame.set_min_date_source(base_dpe_frame.get_entry())
        # # 作成日を契約期限日以降に設定できないよう仕込む
        # base_dpe_frame.set_max_date_source(target_dpe_frame.get_entry())
        
        
        # created_entry = DatePickerEntry(parent, required=True)
        # expiry_entry = DatePickerEntry(parent, required=True)

        # 契約期限は作成日以降しか選べない
        base_dpe_frame.set_max_source(target_dpe_frame)

        # 作成日は契約期限以前しか選べない
        target_dpe_frame.set_min_source(base_dpe_frame)
        
    # ==========================================
    # 要素情報の定義化
    # ==========================================
    def define_field(self):
        # ウィジェット作成と設定に必要な情報を定義
        self.field_definitions = [
            {"column": "quotation_number",     "name": "見積番号",        "ent_type": "",            "required": True},
            {"column": "created_date",         "name": "作成日",          "ent_type": "date_base",   "required": True},
            {"column": "subject",              "name": "件名",            "ent_type": "",            "required": False},
            {"column": "valid_until",          "name": "契約有効期限",    "ent_type": "date",         "required": False},
            {"column": "client_company_name",  "name": "宛先会社名",      "ent_type": "",             "required": True},
            {"column": "client_contact_name",  "name": "宛先担当者名",    "ent_type": "",             "required": False},
            {"column": "notes",                "name": "備考",            "ent_type": "",             "required": False},
        ]
        
        

            
    # ==========================================
    # その他必要な処理
    # ==========================================
    # 前の画面に戻る
    def return_scene(self):
        self.master.show_frame("SceneMain")
        self.reset_entry_list() # 入力中の値をリセットする
        self.reset_data() # 設定した値も初期化する
        self.close_calendar() # カレンダーが開いていたら閉じる
        print("メイン画面に戻ります")
        
    # 次の画面に移る
    def next_scene(self):
        # 必須項目に空欄があれば何もしない
        if self.check_not_null():
            self.check_required_entry_and_focus() # 必須項目欄が空欄なら色を付ける
            return
        
        self.save_temp_data() # データ一時保存
        self.close_calendar() # カレンダーが開いていたら閉じる
        self.master.show_frame("SceneDetailInformation")
        print("明細情報画面に進みます")
        
        
        
        
    # カレンダーが開いていたら閉じる
    def close_calendar(self):
        DatePickerEntry._close_active_popup()
        # for target in self.entry_list:
        #     if target["dpe_frame"] != None:
        #         target["dpe_frame"].destroy_popup()
        
    
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        
        # データが設定されていれば全Entryに書き込む。なければ全Entryをクリアする
        if app_data.quotation_base_data == None:
            self.reset_data()
            self.reset_entry_list()
            self.bot_area.update_msg_box("新規作成")
        else:
            self.data = app_data.quotation_base_data
            self.set_entry_list()
            self.bot_area.update_msg_box("編集中")
            
        # 必須項目欄が空欄なら色を付ける
        self.check_required_entry_and_focus()
        
    
    # ==========================================
    # データ保存：アプリ一時保存用変数にのみ対応（データベースへの保存は別クラスで→プレビューの確定実行時に実行）
    # ==========================================
    # データ一時保存のみ
    def save_temp_data(self):
        # Entryウィジェットの内容をデータベース保存関数に渡す変数に設定
        for data in self.entry_list:
            setattr(self.data, data["column"], data["entry"].get())
        app_data.quotation_base_data = self.data
        
        partial(print, "設定を一時保存しました。")
        
    
    # ==========================================
    # Entryウィジェット処理
    # ==========================================
    def set_entry_list(self):
        for data in self.entry_list:
            data["entry"].delete(0, tk.END)
            data["entry"].insert(0, getattr(self.data, data["column"]))
            
    def reset_entry_list(self):
        for data in self.entry_list:
            data["entry"].delete(0, tk.END)
                
                
                
    # ==========================================
    # 入力規則などの条件管理用関数群
    # ==========================================
    def check_not_null(self):
        for data in self.entry_list:
            if data["required"] == True:
                if data["entry"].get() == "":
                    self.bot_area.update_msg_box("必須項目が空欄になっています。\n入力してください。")
                    return True
        
        # 問題がなければメッセージを空欄にする
        self.bot_area.update_msg_box("")
        return False
    
    # 入力必須Entryが空欄なら目立たせる
    def check_required_entry_and_focus(self, event = None):
        
        for data in self.entry_list:
            if data["required"] == True:
                
                # 全角半角スペースのみの場合、空欄にする（空欄の時は色を付けて目立たせる）
                if data["entry"].get().strip() == "":
                    data["entry"].delete(0, tk.END)
                    data["entry"].config(bg="#FFF0F0")
                else:
                    data["entry"].config(bg="white")
                
            
            
    # ==========================================
    # テーブル定義クラス型の処理
    # ==========================================
    # 初期化
    def reset_data(self):
        self.data = QuotationBaseData(
            quotation_number="",
            created_date="",
            client_company_name="",
        )
        app_data.quotation_base_data = self.data