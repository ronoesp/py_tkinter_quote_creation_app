import tkinter as tk
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from DB.data_base_controller import DatabaseController
from DB.table_data_model import *
from app_data_manager import  AppDataManager

class SceneSetting(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.init_root_frame()
        self.define_field()
        
        self.create_top_area()
        self.create_bot_area()
        self.create_mid_area()
        
        self.reset_data()
        self.load_from_db()
        
    def init_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        
        title = "設定画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)
        
        text = " 戻る "
        self.bot_area.create_button(text, self.return_scene)
        
        text = " 保存 "
        self.bot_area.create_button(text, self.save_to_db)
        
    # ==========================================
    # 3. Middleエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_mid_area(self):
        self.mid_area = mid_area(self)
        self.entry_list = []
        
        # 検証関数をtkinterに登録する（1回登録すれば使い回せる）
        vcmd_natural_num = (self.register(self.validate_natural_numbers), "%P")
        
        for data in self.field_definitions:
            frame = self.mid_area.create_frame_ridge()
            label = self.mid_area.create_label(data["name"], "left")
            entry = self.mid_area.create_entry("right")

            # 正の整数以外を入力不可にする
            if data["ent_type"] == "num_only":
                entry.configure(validate="key", validatecommand=vcmd_natural_num) # キー入力の度にチェック
                
            # 必須項目が目立つように仕込み
            if data["required"] == True:
                new_text = data["name"] + "※"
                label.configure(text=new_text)
                
                # 未入力なら色を付ける
                entry.bind("<FocusOut>", self.check_required_entry_and_focus, add="+")

            self.entry_list.append({"column" : data["column"], "entry" : entry, "required" : data["required"]})
            
            
    # ==========================================
    # 要素情報の定義化
    # ==========================================
    def define_field(self):
        # ウィジェット作成と設定に必要な情報を定義
        self.field_definitions = [
            {"column": "tax_rate",              "name": "消費税率(%)",       "ent_type": "num_only",  "required": True},
            {"column": "delete_grace_days",     "name": "物理削除猶予(日)",  "ent_type": "num_only",  "required": True},
            {"column": "company_name",          "name": "自社名",            "ent_type": "",          "required": True},
            {"column": "company_address",       "name": "自社住所",          "ent_type": "",          "required": False},
            {"column": "company_phone",         "name": "自社電話番号",      "ent_type": "num_only",  "required": False},
            {"column": "company_contact_name",  "name": "自社担当者名",      "ent_type": "",          "required": False},
        ]
        
    # ==========================================
    # その他必要な処理
    # ==========================================
    # 前の画面に戻る
    def return_scene(self):
        self.master.show_frame("SceneMain")
        self.reset_entry_list()
        self.reset_data()
        print("メイン画面に戻ります")
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        self.load_from_db()
        self.bot_area.update_msg_box("")
        
        # 必須項目欄が空欄なら色を付ける
        self.check_required_entry_and_focus()
    
    
    # ==========================================
    # データ読込
    # ==========================================
    # 読込：データベース（アプリ開始時に実行）
    def load_from_db(self):
        # 初回作成時：設定情報テーブルが空欄なら初期データを追加
        data_list = SettingsData.load_conversion_all_data()
        if len(data_list) == 0:
            DatabaseController.table_edit(self.data)
        else:
            # 設定情報テーブルからデータをロード
            self.data = SettingsData.load_conversion_select_data("settings_id", 1)[0]
        
        AppDataManager.settings_data = self.data
        self.set_entry_list()
        
    
    # ==========================================
    # データ保存：※保存はデータベースとアプリ用変数の両方同時に行われる
    # ==========================================
    def save_to_db(self):
        # 必須項目に空欄があれば保存せず終了
        if self.check_not_null():
            return
        
        # Entryウィジェットの内容をデータベース保存関数に渡す変数に設定＆保存
        for data in self.entry_list:
            setattr(self.data, data["column"], data["entry"].get())
        AppDataManager.settings_data = self.data
        
        # データベースに追加or更新が実行される
        DatabaseController.table_edit(self.data)
        
        self.bot_area.update_msg_box("設定を保存しました。")
        
        
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
    # 入力規則チェック：正の整数（自然数）か
    def validate_natural_numbers(self, text):
        return text == "" or text.isdigit()
    
    # 入力規則チェック：必須項目が空欄かチェック
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
        self.data = SettingsData(
            tax_rate=10,
            delete_grace_days=30,
            company_name="未入力", # 必須項目だけど、初期値決められないしどうするかな…一旦これで。
        )