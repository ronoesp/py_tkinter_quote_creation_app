class RecordListNavigator:
    """
    リスト形式のデータとその中の「現在位置(index)」を管理する汎用クラス。

    Tkinterや業務ロジックに一切依存しないため、明細情報画面に限らず、
    「一覧の中の1件を編集しながら前後に移動する」タイプの画面であれば
    どこでも再利用できる。
    """

    def __init__(self, data_list=None):
        self.data_list = data_list if data_list is not None else []
        self.index = 0

    @property
    def current(self):
        """現在選択中のデータを返す"""
        return self.data_list[self.index]

    def reset(self, data_list):
        """データを丸ごと入れ替えて先頭に戻る"""
        self.data_list = data_list
        self.index = 0

    def has_previous(self):
        return self.index > 0

    def has_next(self):
        return self.index < len(self.data_list) - 1

    def move_previous(self):
        if self.has_previous():
            self.index -= 1

    def move_next(self):
        if self.has_next():
            self.index += 1

    def append(self, record):
        """末尾にデータを追加し、そのデータへ移動する"""
        self.data_list.append(record)
        self.index = len(self.data_list) - 1

    def remove_current(self):
        """
        現在選択中のデータを削除する。
        要素が1件しかない場合は削除せず False を返す。
        """
        if len(self.data_list) <= 1:
            return False

        self.data_list.pop(self.index)
        if self.index >= len(self.data_list):
            self.index = len(self.data_list) - 1
        return True

    def position_label(self):
        """「2 / 5」のような現在位置の表示文字列を返す"""
        return f"{self.index + 1} / {len(self.data_list)}"
