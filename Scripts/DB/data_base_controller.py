import sqlite3
import atexit
import os
import sys
from dataclasses import astuple
from .table_data_model import *
from .table_define import TableDefine

class DatabaseController():
    # クラス変数
    conn: sqlite3.Connection = None  # クラス変数として接続を保持
    db_name: str = 'MITUMORI.sqlite3'
    relative_dir: str = 'DB'
    
    
    # ==========================================
    # データベース準備（作成/接続/自動終了設定）
    # ==========================================
    
    @classmethod
    def init_db(cls):
        if cls.conn is not None:
            raise RuntimeError("TableDataController.init()は既に実行済みです。複数回呼び出さないでください。")
        
        cls._connect_db()   # データベースへのアクセス（なければ作成も実施）
        cls._create_table() # テーブル作成（すでにあれば何もしない）
        cls._close_db()     # アプリ終了時にデータベースを自動で閉じるように設定
    
    # データベースへアクセス（データベースがない場合は自動で作成される）
    @classmethod
    def _connect_db(cls):
            
        if getattr(sys, 'frozen', False):
            # exe化されている場合 → exe自身の場所
            base_dir = os.path.dirname(sys.executable)
        else:
            # .pyのまま実行している場合
            main_file = sys.modules['__main__'].__file__
            base_dir = os.path.dirname(os.path.abspath(main_file))
        
        # DBフォルダが無ければ作成する
        db_dir = os.path.join(base_dir, cls.relative_dir)
        os.makedirs(db_dir, exist_ok=True)
        
        # DB接続（DBがなければ作成してから接続される）
        dbname = os.path.join(db_dir, cls.db_name)
        cls.conn = sqlite3.connect(dbname)
    
    # アプリ終了時にデータベースへのコネクションを閉じるように設定(必須)
    @classmethod
    def _close_db(cls):
        atexit.register(cls.conn.close)
        
    # テーブル作成のための命令文を組み立てる
    @classmethod
    def _table_ddl(cls, table_name, table_dict):
        top_str = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
        bot_str = ")"
        mid_str = ""
        
        for data in table_dict:
            mid_str = mid_str + data["name"] + " " + data["type"] + " " + data["constraints"] + ","
        mid_str = mid_str[:-1]
        
        return top_str + mid_str + bot_str
    
    # テーブルを作成（既にあるテーブルは作成されない）
    @classmethod
    def _create_table(cls):
        cur = cls.conn.cursor()
        
        for data in TableDefine.table_define_dict_list():
            query = cls._table_ddl(data["table_name"], data["columns"])
            cur.execute(query)
    
    
    
    # ==========================================
    # データベース操作（作成/編集/読込/削除）
    # ==========================================
    
    # テーブル操作：レコード追加or編集
    @classmethod
    def table_edit(cls, data):
        cur = cls.conn.cursor()

        pk = data.get_pk()
        exists = False
        if pk is not None:
            cur.execute(data.EXISTS_SQL, data.exists_params())
            exists = cur.fetchone()[0] > 0 # fetchone()：直前に実行したSELECT文の結果から、1行だけ取得するメソッドです。

        if exists:
            cur.execute(data.UPDATE_SQL, data.update_values())
        else:
            cur.execute(data.INSERT_SQL, data.insert_values())
            data.set_pk(cur.lastrowid)  # 新規作成したIDをdata側に反映しておく

        cls.conn.commit()
        
    # テーブル操作：レコード取得(辞書型を1件返す)
    @classmethod
    def get_record(cls, table_name, pk_column, pk_value):
        cur = cls.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {pk_column} = ?", (pk_value,))
        row = cur.fetchone()

        if row is None:
            return None  # 該当するレコードがない場合

        column_names = [description[0] for description in cur.description]
        return dict(zip(column_names, row))
    
        # 使用例
        # settings = self.get_record("settings", "settings_id", 1)
        # quotation = self.get_record("quotation_base", "quotation_id", 3)
        
    # テーブル操作：レコード取得(辞書型を複数件返す)
    @classmethod
    def get_records_by(cls, table_name, column_name, value):
        """指定した条件に一致する、複数件のレコードを辞書のリストで取得する"""
        cur = cls.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {column_name} = ?", (value,))
        rows = cur.fetchall()  # ← 複数件取得する

        column_names = [description[0] for description in cur.description]
        return [dict(zip(column_names, row)) for row in rows]
    
    # テーブル操作：部分一致検索
    @classmethod
    def search_records(cls, table_name, column_name, keyword):
        """指定した列に対して、部分一致(LIKE)でレコードを検索する"""
        cur = cls.conn.cursor()
        like_pattern = f"%{keyword}%"
        cur.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?", (like_pattern,))
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]
        return [dict(zip(column_names, row)) for row in rows]
        
        
    # テーブル操作：レコード削除
    @classmethod
    def delete_record(cls, table_name, pk_column, pk_value):
        cur = cls.conn.cursor()
        cur.execute(f"DELETE FROM {table_name} WHERE {pk_column} = ?", (pk_value,))
        cls.conn.commit()
        
        
        
    # ==========================================
    # デバッグ用関数（テーブル存在確認/テーブル列構成確認/テーブルデータ一覧確認）
    # ==========================================
    
    # テーブルが存在するか確認（必要に応じて修正：今のところデバッグ用）
    @classmethod
    def check_exist_table(cls, table_name: str):
        cur = cls.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
        print(table_name + "テーブルの存在:", cur.fetchall())
        
        
    # テーブルの列構成を確認
    @classmethod
    def check_table_column_structure(cls, table_name: str):
        cur = cls.conn.cursor()
        print("[" + table_name + "]")
        print("==========================")
        cur.execute("PRAGMA table_info(" + table_name + ")")
        for row in cur.fetchall():
            print(row)
        print("==========================")
    
        
    # テーブルの中身をすべて表示（必要に応じて修正：今のところデバッグ用）
    @classmethod
    def show_table(cls, table_name):
        cur = cls.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]

        print(f"--- {table_name} ---")
        for row in rows:
            print(dict(zip(column_names, row)))
            
    @classmethod
    def get_all_records(cls, table_name):
        cur = cls.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]
        return [dict(zip(column_names, row)) for row in rows]
                
    