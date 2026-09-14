import tkinter as tk
from functools import partial
from GUI.component_area_top import ComponentAreaTop as top_area
from GUI.component_area_bot import ComponentAreaBot as bot_area
from GUI.component_area_mid import ComponentAreaMid as mid_area
from GUI.component_area_page_controll import ComponentAreaPageControll as page_ctr_area
from DB.table_data_model import QuotationBaseData, QuotationDetailData
from app_data_manager import AppDataManager as app_data

class SceneHistoryList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # データベースからレコード一覧を取得するための変数
        self.db_quote_list = []
        self.db_detail_list = []
        
        # 履歴情報を表示するTextウィジェットリスト
        self.text_area_list = []
        
        # 現在のページ（ページは1以上の値にする）
        self.now_page = 1
        
        # ソートフラグ：昇順降順
        self.reverse_sort_flg_number = False
        self.reverse_sort_flg_date = False
        
        self.init_root_frame()
        self.create_top_area()
        self.create_bot_area()
        self.create_page_ctr_area()
        self.create_mid_area()
        
        
    def init_root_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
    # ==========================================
    # 1. TOPエリア（画面タイトル）
    # ==========================================
    def create_top_area(self):
        title = "履歴画面"
        self.top_area = top_area(self, title)
        
    # ==========================================
    # 2. BOTTOMエリア（フッター・ボタン等）
    # ==========================================
    def create_bot_area(self):
        self.bot_area = bot_area(self, show_msg_box=False)
        
        text = " 戻る "
        self.bot_area.create_button(text, self._return_scene)
        
    # ==========================================
    # 3. Middleエリア（スクロール可能なCanvas領域）
    # ==========================================
    def create_mid_area(self):
        self.mid_area = mid_area(self)
        
        # 1.検索欄
        self.mid_area.create_frame_ridge()
        self.mid_area.create_label("検索", "left")
        self.ent_serch = self.mid_area.create_entry("right")
        self.ent_serch.bind("<Return>", self._serch)  # Enterキーで実行
        
        # 2.ソート欄
        self.mid_area.create_frame_ridge()
        self.mid_area.create_button("見積番号", self._sort_quote_number, "left")
        self.mid_area.create_button(" 更新日 ", self._sort_quote_date, "left")
        self.mid_area.create_label("件名", "left")
        
        # 3.データ欄
        show_data_num = 4 # 1ページに表示する履歴の数
        for i in range(show_data_num):
            self.mid_area.create_frame_ridge()
            txt =self.mid_area.create_text_normal("left")
            
            cmd = partial(self._select_data, i)
            self.mid_area.create_button(" 選択 ", cmd, "right")
            
            self.text_area_list.append(txt)
        
    # ==========================================
    # 4. ページ切り替えエリア
    # ==========================================
    def create_page_ctr_area(self):
        self.page_ctr_area = page_ctr_area(self)
        self.page_ctr_area.set_cmd_button(self.prev_page, self.next_page)
    
    
    
        
        
        
        
        
        
    # データ選択：index番目に表示されている見積データを選択し、履歴プレビュー画面に飛ぶ
    def _select_data(self, index):
        data_num = len(self.db_quote_list)
        area_num = len(self.text_area_list)
        data_index = area_num * ( self.now_page - 1) + index
        
        if data_index >= data_num:
            return
        
        # 見積書IDから明細情報リストを受け取る
        id = self.db_quote_list[data_index].quotation_id
        self.db_detail_list = QuotationDetailData.load_conversion_select_data("quotation_id", id)
        
        # 選択した見積書情報を一時保存
        app_data.quotation_base_data = self.db_quote_list[data_index]
        app_data.quotation_detail_data_list = self.db_detail_list
        
        self.master.show_frame("SceneShowHistory")
        print("データを選択しました")
        
        
    # 前の画面に戻る
    def _return_scene(self):
        self.master.show_frame("SceneMain")
        print("メイン画面に戻ります")
        
    # 再表示された時に実行される関数(すべてのシーンに実装する：スーパークラス作って共通化したいところ)
    def init_active(self):
        self.now_page = 1
        self.db_quote_list = QuotationBaseData.load_conversion_all_data()
        self._update_label_page_info()
        self._update_history_text()
        
        
    
    # ==========================================
    # ページ操作関連
    # ==========================================
    # ページの最大数を返す
    def _max_page_num(self):
        data_num = len(self.db_quote_list)
        area_num = len(self.text_area_list)
        
        # A // B で整数値となる（負の値の時は結果が変わるので仕様を確認すること）
        if data_num % area_num != 0:
            max_page_num = (data_num // area_num) + 1
        else:
            max_page_num = (data_num // area_num)
            
        if max_page_num == 0:
            max_page_num = 1
            
        return max_page_num
    
    # ページを範囲内に収める
    def _clamp_now_page(self):
        # self.now_pageが最大ページ数を超えていたら、最後のページに設定する
        if self.now_page > self._max_page_num():
            self.now_page = self._max_page_num()
        
    # ページ表記更新（何ページ目かがわかるようにする）
    def _update_label_page_info(self):
        new_text = str(self.now_page) + "/" + str(self._max_page_num())
        self.page_ctr_area.update_center_text(new_text)
        
    def prev_page(self):
        if self.now_page <= 1:
            return
        
        self.now_page = self.now_page - 1
        self._update_label_page_info()
        self._update_history_text()
        print("前のページに戻ります")
        
    def next_page(self):
        if self.now_page >= self._max_page_num():
            return
        
        self.now_page = self.now_page + 1
        self._update_label_page_info()
        self._update_history_text()
        print("次のページに進みます")
        

    # ==========================================
    # 検索
    # ==========================================
    def _serch(self, event=None):
        self._search_by_subject()
        self._clamp_now_page()
        self._update_label_page_info()
        self._update_history_text()
        
    # 検索：subjectカラムでの部分一致検索
    def _search_by_subject(self):
        keyword = self.ent_serch.get()

        if keyword:
            self.db_quote_list = QuotationBaseData.load_conversion_serch_data("subject", keyword)
        else:
            self.db_quote_list = QuotationBaseData.load_conversion_all_data()
        
    
    # ==========================================
    # ソート処理
    # ==========================================
    def _sort_quote_number(self):
        self._sort_from_number()
        self._update_history_text()
        
    def _sort_quote_date(self):
        self._sort_from_date()
        self._update_history_text()
        
    def _sort_from_number(self):
        # 昇降順切り替え
        self.reverse_sort_flg_number = not self.reverse_sort_flg_number
        
        # ソート実行
        self.db_quote_list = sorted(
            self.db_quote_list,
            key=lambda s: int(s.quotation_number),
            reverse=self.reverse_sort_flg_number)
        
    def _sort_from_date(self):
        # 昇降順切り替え
        self.reverse_sort_flg_date = not self.reverse_sort_flg_date
        
        # ソート実行
        self.db_quote_list = sorted(
            self.db_quote_list,
            key=lambda s: s.created_date,
            reverse=self.reverse_sort_flg_date)
    
    # ==========================================
    # 履歴テキスト作成
    # ==========================================
    def _update_history_text(self):
        data_num = len(self.db_quote_list)
        area_num = len(self.text_area_list)
        
        for i in range( area_num ):
            first_index = area_num * (self.now_page - 1)
            if first_index + i < data_num:
                data = self.db_quote_list[first_index + i]
                
                # テキスト作成
                new_text = ""
                new_text = new_text + data.quotation_number + " : "
                new_text = new_text + data.created_date + " : "
                new_text = new_text + data.subject
                
                # テキストウィジェット更新
                self.text_area_list[i].configure(state="normal")   # 一時的に編集可能にする
                self.text_area_list[i].delete("1.0", tk.END)   # 先頭から末尾まで全部消す
                self.text_area_list[i].insert("1.0", new_text)  # 先頭に新しい文字列を挿入する
                self.text_area_list[i].configure(state="disabled")  # 再び編集不可に戻す
            else:
                # クリア処理
                self.text_area_list[i].configure(state="normal")   # 一時的に編集可能にする
                self.text_area_list[i].delete("1.0", tk.END)   # 先頭から末尾まで全部消す
                self.text_area_list[i].configure(state="disabled")  # 再び編集不可に戻す