import tkinter as tk

class ComponentStyle:
    """アプリ全体で共通する色・フォント定義"""

    # ==========================================
    # フォント定義(ベースファミリーを1箇所で管理)
    # ==========================================
    FONT_FAMILY = "Yu Gothic UI"

    FONT_TEXT = (FONT_FAMILY, 10)                    # 通常テキスト
    FONT_BUTTON = (FONT_FAMILY, 9)                    # 通常ボタン
    FONT_SECTION_TITLE = (FONT_FAMILY, 14, "bold")    # セクション見出し
    FONT_MENU_BUTTON = (FONT_FAMILY, 12)              # メイン画面の大ボタン
    FONT_MAIN_TITLE = (FONT_FAMILY, 22, "bold")       # メイン画面タイトル
    FONT_SUB_TITLE = (FONT_FAMILY, 11)                # メイン画面サブタイトル

    # ==========================================
    # 色定義
    # ==========================================
    PRIMARY_BG = "#dddddd"
    LABEL_BG = "whitesmoke"
    REQUIRED_BG = "#FFF0F0"
    REQUIRED_BORDER = "#E74C3C"
    NORMAL_BORDER = "gray"

    TITLE_BG = "#333333"
    TITLE_FG = "white"

    MENU_BTN_BORDER = "#cccccc"
    MAIN_BG = "#ffffff"
    MAIN_TITLE_FG = "#222222"
    SUB_TITLE_FG = "#888888"

    DARK_BG = "#2e2e2e"
    DARK_FG = "#ffffff"

    # ==========================================
    # 汎用パーツ
    # ==========================================
    @classmethod
    def style_frame_ridge(cls, component: tk.Frame):
        component.configure(
            bg=cls.LABEL_BG,
            padx=10,
            pady=5,
            relief="ridge",
            bd=1  # bd(borderwidthの略)は、フレームの枠線の太さをピクセル単位で指定するオプション
        )

    # 横幅は文字数で自動設定させる(サイズを合わせる場合はスペースを使用)
    @classmethod
    def style_button(cls, component):
        component.configure(
            font=cls.FONT_BUTTON,
            padx=10,
            pady=5
        )

    @classmethod
    def style_label_title(cls, component):
        component.configure(
            bg=cls.TITLE_BG,
            fg=cls.TITLE_FG,
            font=cls.FONT_SECTION_TITLE
        )

    @classmethod
    def style_label_msg_box(cls, component):
        component.configure(
            font=cls.FONT_TEXT,
            bg="white",
            fg="black",
            width=35,
            height=3,
            wraplength=300,
            justify="left",
            anchor='center'
        )

    @classmethod
    def style_text_normal(cls, component):
        component.configure(
            font=cls.FONT_TEXT,
            bg="white",
            fg="black",
            width=50,
            height=1,
            padx=10,
            pady=10,
            wrap="word",
            state="disabled"
        )

    @classmethod
    def style_text_dark(cls, component):
        component.configure(
            font=cls.FONT_TEXT,          # フォントとサイズ
            bg=cls.DARK_BG,               # 背景色(ダークグレー)
            fg=cls.DARK_FG,               # 文字色(白)
            insertbackground="white",     # カーソルの色
            padx=10,                      # 内側の横パディング
            pady=10,                      # 内側の縦パディング
            relief="flat",                # 枠線のスタイル(flat, ridge, groove, raised, sunken)
            wrap="none"                   # ← 日本語の予期せぬ自動折り返しを防ぐために追加
        )

    # ==========================================
    # メイン画面用
    # ==========================================
    @classmethod
    def style_button_main_manue(cls, component):
        component.configure(
            width=16,
            height=4,
            font=cls.FONT_MENU_BUTTON,
            bg=cls.MAIN_BG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=cls.MENU_BTN_BORDER
        )

    @classmethod
    def style_label_main_title(cls, component):
        component.configure(
            font=cls.FONT_MAIN_TITLE,
            bg=cls.MAIN_BG,
            fg=cls.MAIN_TITLE_FG
        )

    @classmethod
    def style_label_sub_title(cls, component):
        component.configure(
            font=cls.FONT_SUB_TITLE,
            bg=cls.MAIN_BG,
            fg=cls.SUB_TITLE_FG
        )