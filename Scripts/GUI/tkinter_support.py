import tkinter as tk

# ==========================================
# tkinterをサポートする機能群
# ==========================================
class TkinterSupport():
    
    # ==========================================
    # TEXT：ウィンドウサイズは変えず、Textウィジェットのサイズだけをピクセル単位で自動調整する
    # ==========================================
    @staticmethod
    def _adjust_text_widget_size(target_text: tk.Text):
        # 1. テキスト内容を取得（末尾の自動改行を除く）
        content = target_text.get("1.0", "end - 1c")
        lines = content.split("\n")
        
        # 2. 行数を計算（最低1行）
        num_lines = len(lines) if lines else 1
        
        # 3. 日本語（全角）を2文字、半角を1文字としてカウントして最大幅を計算
        max_char_width = 0
        for line in lines:
            # 各行のバイト数に似た長さを計算（全角を2、半角を1としてカウント）
            # len(line.encode('cp932')) を使うと、日本語を2文字分として正確に数えられます
            char_width = len(line.encode('cp932'))
            if char_width > max_char_width:
                max_char_width = char_width
                
        # tk.Text の width オプションは「半角文字数」単位なので、計算した値をそのまま使えます
        # 最低限の幅（例: 10文字分）を保証
        final_width = max(max_char_width, 10)
        final_height = num_lines
        
        # 4. config を使って Text ウィジェット自体の設定値を更新（これなら pack されても潰れません）
        target_text.config(width=final_width, height=final_height)
    
    @staticmethod
    def set_text(new_text : str, target_text: tk.Text):
        target_text.configure(state="normal")  # 一時的に解除
        target_text.delete("1.0", "end")
        target_text.insert("1.0", new_text)
        target_text.configure(state="disabled")  # また閉じる
    
    @classmethod
    def set_text_adjust(cls, new_text : str, target_text: tk.Text):
        cls.set_text(new_text, target_text)
        cls._adjust_text_widget_size(target_text)