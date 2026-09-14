import tkinter as tk
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from GUI.component_area_page_controll import ComponentAreaPageControll as page_ctr_area
from GUI.entry_form_manager import EntryFormManager
from common.record_list_navigator import RecordListNavigator
from DB.table_data_model import *
from app_data_manager import AppDataManager as app_data


class SceneDetailInformation(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_root_frame()
        self.define_field()

        self.create_top_area()
        self.create_bot_area()
        self.create_page_ctr_area()
        self.create_mid_area()

        self.pager = RecordListNavigator()
        self.form.bind_on_change(lambda d: d["is_calc_data"], "<FocusOut>", self.calc_amount)

    def init_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        title = "明細情報画面"
        self.top_area = top_area(self, title)

    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self)

        self.bot_area.create_button(" 戻る ", self.return_scene)
        self.bot_area.create_button(" 次へ ", self.next_scene)
        self.bot_area.create_button(" 削除 ", self.delete_data)
        self.bot_area.create_button(" 追加 ", self.add_data)

    # ==========================================
    # 3. Middleエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_mid_area(self):
        self.mid_area = mid_area(self)
        self.form = EntryFormManager(self.mid_area, self.field_definitions, self.register)
        self.form.build()

    # ==========================================
    # 4. ページ切り替えエリア
    # ==========================================
    def create_page_ctr_area(self):
        self.page_ctr_area = page_ctr_area(self)
        self.page_ctr_area.set_cmd_button(self.pre_page, self.next_page)

    # ==========================================
    # 要素情報の定義化
    # ==========================================
    def define_field(self):
        self.field_definitions = [
            {"column": "item_name",   "name": "品目名",     "ent_type": "",         "required": True,  "is_calc_data": False},
            {"column": "unit",        "name": "単位",       "ent_type": "",         "required": False, "is_calc_data": False},
            {"column": "unit_price",  "name": "単価",       "ent_type": "num_only", "required": True,  "is_calc_data": True},
            {"column": "quantity",    "name": "数量",       "ent_type": "num_only", "required": True,  "is_calc_data": True},
            {"column": "tax_rate",    "name": "税率（％）", "ent_type": "tax_rate", "required": False, "is_calc_data": False},
            {"column": "amount",      "name": "金額",       "ent_type": "calc",     "required": False, "is_calc_data": False},
            {"column": "description", "name": "内容 / 説明", "ent_type": "",        "required": False, "is_calc_data": False},
        ]

    # ==========================================
    # 計算関連（この画面固有の業務ロジック）
    # ==========================================
    def unlock_calculated_entries(self):
        """税率・合計欄を編集可能に戻す（値を書き換える前に呼ぶ）"""
        self.form.set_state("tax_rate", "normal")
        self.form.set_state("amount", "normal")

    def lock_calculated_entries(self):
        """税率をdataから再設定し、税率・合計欄を編集不可にする"""
        self.form.set_value("tax_rate", self.pager.current.tax_rate, state="readonly")
        self.form.set_value("amount", "", state="readonly")

    def finalize_calculated_entries(self):
        """税率・合計欄をロックし、金額を再計算する（切替/追加/削除の最後にまとめて呼ぶ）"""
        self.lock_calculated_entries()
        self.calc_amount()

    def calc_amount(self, event=None):
        unit_price = self.form.get_value("unit_price")
        quantity = self.form.get_value("quantity")
        tax_rate = self.form.get_value("tax_rate")

        if unit_price == "" or quantity == "":
            return

        tax_multiplier = 100 + int(tax_rate)
        amount = int(int(unit_price) * int(quantity) * tax_multiplier / 100)

        self.form.set_value("amount", str(amount), state="readonly")

    # ==========================================
    # その他必要な処理
    # ==========================================
    def _has_empty_required_field(self):
        """必須項目が空欄ならメッセージ表示とハイライトを行い True を返す"""
        if self.form.has_empty_required():
            self.bot_area.update_msg_box("必須項目が空欄になっています。\n入力してください。")
            self.form.highlight_required()
            return True

        self.bot_area.update_msg_box("")
        return False

    def _new_detail_data(self):
        return QuotationDetailData(
            quotation_id=0,  # 新規作成/編集で変わる：新規=NULLor-1 / 編集：DBから取得した値
            item_name="",
            unit_price=0,
            quantity=0,
            tax_rate=0,
            amount=0,
        )

    def return_scene(self):
        if self._has_empty_required_field():
            return

        self.form.save_to(self.pager.current)
        self.form.clear()
        self.master.show_frame("SceneBasicQuoteInformation")
        print("見積基本情報画面に戻ります")

    def next_scene(self):
        if self._has_empty_required_field():
            return

        self.form.save_to(self.pager.current)
        app_data.quotation_detail_data_list = self.pager.data_list  # ※データの完全一時保存はここでのみ行う
        self.master.show_frame("ScenePreview")
        print("プレビュー画面へ移動します")

    def add_data(self):
        if self._has_empty_required_field():
            return

        self.unlock_calculated_entries()

        self.form.save_to(self.pager.current)
        new_data = self._new_detail_data()
        self.pager.append(new_data)
        self.form.clear()
        self.update_label_page_info()

        # 明細追加時は、設定情報の税率を初期値として設定する
        new_data.tax_rate = app_data.settings_data.tax_rate
        self.finalize_calculated_entries()

        self.form.highlight_required()
        print("明細情報を追加します")

    def delete_data(self):
        if len(self.pager.data_list) <= 1:
            self.bot_area.update_msg_box("削除できません。\nデータは１つ以上必要です。")
            return

        # 確認画面（サブウィンドウ）を表示する
        self.master.change_sub_window_state()
        self.master.wait_variable(app_data.decide_result)  # ★変数が変化するまでここで待機

        if app_data.decide_result.get():
            self.unlock_calculated_entries()

            self.pager.remove_current()
            self.form.load_from(self.pager.current)
            self.update_label_page_info()

            self.finalize_calculated_entries()
            self.form.highlight_required()
        else:
            print("いいえが選択されました")

        app_data.decide_result.set(False)

    def init_active(self):
        """再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)"""
        self.bot_area.update_msg_box("見積基本情報の設定が完了しました。\n明細情報を設定してください。")

        self.unlock_calculated_entries()

        if app_data.quotation_detail_data_list == []:
            self.pager.reset([self._new_detail_data()])
            app_data.quotation_detail_data_list = self.pager.data_list
            self.form.clear()
            self.pager.current.tax_rate = app_data.settings_data.tax_rate
        else:
            self.pager.reset(app_data.quotation_detail_data_list)
            self.form.load_from(self.pager.current)

        self.update_label_page_info()
        self.finalize_calculated_entries()
        self.form.highlight_required()

    # ==========================================
    # ページ変更処理
    # ==========================================
    def update_label_page_info(self):
        self.page_ctr_area.update_center_text(self.pager.position_label())

    def _switch_page(self, move):
        """move: pager.move_previous または pager.move_next を渡す"""
        self.unlock_calculated_entries()

        self.form.save_to(self.pager.current)
        move()
        self.form.load_from(self.pager.current)
        self.update_label_page_info()

        self.finalize_calculated_entries()

    def pre_page(self):
        if self._has_empty_required_field():
            return

        if self.pager.has_previous():
            self._switch_page(self.pager.move_previous)

    def next_page(self):
        if self._has_empty_required_field():
            return

        if self.pager.has_next():
            self._switch_page(self.pager.move_next)
