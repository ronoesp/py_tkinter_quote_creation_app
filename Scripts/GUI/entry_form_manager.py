import tkinter as tk


class EntryFormManager:
    """
    field_definitions（column/name/ent_type/required等を持つdictのリスト）を元に
    Entry群を構築し、値の取得・設定・必須チェック・ハイライトをまとめて行う汎用クラス。

    各画面固有の項目定義（品目名・単価…など）はfield_definitionsとして外から渡すだけで、
    このクラス自体は「見積の明細」であることを一切知らない＝他の入力画面でも再利用できる。
    """

    def __init__(self, container, field_definitions, register_func):
        self.container = container
        self.field_definitions = field_definitions
        self.register_func = register_func  # tk.Widget.register（%P検証用）
        self.entry_list = []
        self.entries_by_column = {}

    # ==========================================
    # 構築
    # ==========================================
    def build(self):
        vcmd_natural_num = (self.register_func(self.validate_number), "%P")

        for data in self.field_definitions:
            self.container.create_frame_ridge()
            label = self.container.create_label(data["name"], "left")
            entry = self.container.create_entry("right")

            if data.get("ent_type") == "num_only":
                entry.configure(validate="key", validatecommand=vcmd_natural_num)

            if data.get("required"):
                label.configure(text=data["name"] + "※")
                entry.bind("<FocusOut>", self.highlight_required, add="+")

            field = dict(data)
            field["entry"] = entry
            self.entry_list.append(field)
            self.entries_by_column[data["column"]] = entry

    def bind_on_change(self, predicate, event, handler):
        """predicate(field_dict)がTrueを返す項目のEntryにイベントを仕込む"""
        for data in self.entry_list:
            if predicate(data):
                data["entry"].bind(event, handler, add="+")

    # ==========================================
    # 値の取得・設定
    # ==========================================
    @staticmethod
    def validate_number(text):
        """空文字、または数字のみで構成されているならOK"""
        return text == "" or text.isdigit()

    def get_value(self, column):
        return self.entries_by_column[column].get()

    def set_value(self, column, value, state=None):
        """指定カラムのEntryへ値を設定する（読み取り専用の解除・再設定も行う）"""
        entry = self.entries_by_column[column]
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        if state:
            entry.config(state=state)

    def set_state(self, column, state):
        self.entries_by_column[column].config(state=state)

    def load_from(self, obj):
        """オブジェクトの属性値を各Entryへ反映する"""
        for data in self.entry_list:
            self.set_value(data["column"], getattr(obj, data["column"]))

    def save_to(self, obj):
        """各Entryの入力値をオブジェクトの属性へ反映する"""
        for data in self.entry_list:
            setattr(obj, data["column"], self.entries_by_column[data["column"]].get())

    def clear(self):
        for data in self.entry_list:
            data["entry"].delete(0, tk.END)

    # ==========================================
    # 必須項目チェック
    # ==========================================
    def has_empty_required(self):
        return any(
            data["required"] and self.entries_by_column[data["column"]].get() == ""
            for data in self.entry_list
        )

    def highlight_required(self, event=None):
        """必須Entryが空欄なら目立たせる（全角半角スペースのみの場合も空欄扱い）"""
        for data in self.entry_list:
            if data["required"]:
                entry = self.entries_by_column[data["column"]]
                if entry.get().strip() == "":
                    entry.delete(0, tk.END)
                    entry.config(bg="#FFF0F0")
                else:
                    entry.config(bg="white")
