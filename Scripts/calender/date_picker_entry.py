import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime


class DatePickerEntry(tk.Frame):
    """
    ボタン+Entryで構成される日付入力欄。
    ・ボタンでカレンダーを開いて選択、Entryへの直接入力も可能
    ・他のDatePickerEntryをmin_source/max_sourceとして紐付けると、
      相手の入力値を選択可能範囲の制限として使える
      (例: 契約期限側にset_min_source(作成日側)を設定すると、
       契約期限は作成日以降しか選べなくなる)
    """

    DATE_FORMAT = "%Y/%m/%d"          # Python標準のstrptime/strftime用
    CAL_DATE_PATTERN = "yyyy/mm/dd"   # tkcalendar用(書式の指定ルールが異なるので別で持つ)
    _active_popup = None  # ← クラス変数:全インスタンスで共有する「今開いているポップアップ」

    def __init__(self, parent, required=False):
        super().__init__(parent)
        self.required = required
        self.min_source = None  # これより前の日付は選べない
        self.max_source = None  # これより後の日付は選べない
        # _active_popup = None

        self.btn = tk.Button(self, text="📅", command=self.open_calendar)
        self.btn.pack(side="left", padx=5)

        self.entry = tk.Entry(self, width=15)
        self.entry.pack(side="left")
        self.entry.bind("<FocusOut>", self._validate_entry)

    # ---- 他のDatePickerEntryとの連携設定 ----
    def set_min_source(self, other):
        self.min_source = other

    def set_max_source(self, other):
        self.max_source = other

    # ---- 値の取得 ----
    def get_date(self):
        """入力値をdateとして返す。空欄・不正な値ならNone"""
        return self._parse(self.entry.get())

    def get_entry(self):
        return self.entry

    # ---- カレンダー表示 ----
    def open_calendar(self):
        # self._close_popup()
        DatePickerEntry._close_active_popup()  # ← 自分ではなく、クラス全体で1つだけ閉じる

        top = tk.Toplevel(self)
        top.withdraw()  # 位置決め前に表示させない
        top.title("日付選択")
        top.transient(self.winfo_toplevel())
        top.resizable(False, False)

        mindate = self.min_source.get_date() if self.min_source else None
        maxdate = self.max_source.get_date() if self.max_source else None
        
        print(mindate)
        print(maxdate)

        cal = Calendar(top, selectmode="day", date_pattern="yyyy/mm/dd", mindate=mindate, maxdate=maxdate)
        cal.pack()
        cal.bind("<<CalendarSelected>>", lambda e: self._on_select(cal, top))

        x = self.btn.winfo_rootx()
        y = self.btn.winfo_rooty() + self.btn.winfo_height()
        top.geometry(f"+{x}+{y}")
        top.deiconify()
        top.lift()
        
        DatePickerEntry._active_popup = top

    def _on_select(self, cal, popup):
        self._set_value(cal.get_date())
        DatePickerEntry._close_active_popup()

    @classmethod
    def _close_active_popup(cls):
        if cls._active_popup is not None and cls._active_popup.winfo_exists():
            cls._active_popup.destroy()
        cls._active_popup = None

    # ---- 手入力の検証 ----
    def _validate_entry(self, event=None):
        value = self.entry.get().strip()
        if value == "":
            self._apply_required_style()
            return

        parsed = self._parse(value)
        if parsed is None or not self._within_range(parsed):
            self.entry.delete(0, tk.END)
        else:
            self._set_value(parsed.strftime(self.DATE_FORMAT))

        self._apply_required_style()

    def _within_range(self, target_date) -> bool:
        mindate = self.min_source.get_date() if self.min_source else None
        maxdate = self.max_source.get_date() if self.max_source else None
        if mindate and target_date < mindate:
            return False
        if maxdate and target_date > maxdate:
            return False
        return True

    @staticmethod
    def _parse(value: str):
        for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y%m%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    def _set_value(self, date_str: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, date_str)
        self._apply_required_style()

    def _apply_required_style(self):
        if not self.required:
            return
        self.entry.config(bg="#FFF0F0" if self.entry.get().strip() == "" else "white")