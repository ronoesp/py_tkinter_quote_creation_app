# 見積書作成アプリ（py_tkinter_quote_creation_app）

Tkinterで作成した簡易見積書作成アプリのリポジトリです。

**PC版（インストーラー）のダウンロード**
https://github.com/ronoesp/py_tkinter_quote_creation_app/releases/latest

---

## 提供しているバージョン

| バージョン | 実行環境 | 特徴 |
|---|---|---|
| PC版 | Windows（要インストール） | Tkinter製。exe/インストーラーをReleasesで配布 |

## フォルダ構成

```
py_tkinter_quote_creation_app/
├── scripts/              # PC版（Tkinter）のソースコード
├── docs-project/          # 要件定義書・詳細設計書
├── notes/                 # 学習メモ
└── README.md              # このファイル
```

## 実行方法

### PC版
[Releases](https://github.com/ronoesp/py_tkinter_quote_creation_app/releases/latest) からインストーラーをダウンロードし、実行してください。

## 制作環境
・言語：Python3
・GUI：Tkinter
・DB：SQLite
・エディタ：VisualStudioCode

## その他
・scripts フォルダの app_quote_creation.py から実行可能

※実行すると同階層に「DB」フォルダが作成され、この中にデータベースファイルが作成される。
