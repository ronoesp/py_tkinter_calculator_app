# 電卓アプリ（py_tkinter_calculator_app）

Tkinterで作成したPython電卓アプリと、そのWeb版（2種類）をまとめたリポジトリです。

**公開ページ（3種類を選べる案内ページ）**
https://ronoesp.github.io/py_tkinter_calculator_app/app

**PC版（インストーラー）のダウンロード**
https://github.com/ronoesp/py_tkinter_calculator_app/releases/latest

---

## 提供している3つのバージョン

| バージョン | 実行環境 | 特徴 |
|---|---|---|
| PC版 | Windows（要インストール） | Tkinter製。exe/インストーラーをReleasesで配布 |
| Web版（Pyodide） | ブラウザのみ | PythonロジックをPyodide経由でブラウザ内実行 |
| Web版（PyScript） | ブラウザのみ | 同じロジックをPyScriptフレームワークで実装 |

Web版はどちらもサーバーを使わず、計算処理はすべて利用者のブラウザ内で完結します。そのため複数人が同時にアクセスしても、他の利用者との競合は発生しません。

## フォルダ構成

```
py_tkinter_calculator_app/
├── index.html          # 案内ページ（GitHub Pages）
├── style.css
├── webapp-pyodide/      # Web版（Pyodide）一式
├── webapp-pyscript/      # Web版（PyScript）一式
├── desktop/              # PC版（Tkinter）のソースコード
├── docs-project/          # 要件定義書・詳細設計書
├── notes/                 # 学習メモ
├── backup/                # 過去バージョンのバックアップ
└── README.md              # このファイル
```

## 各バージョンの実行方法

### PC版
[Releases](https://github.com/ronoesp/py_tkinter_calculator_app/releases/latest) からインストーラーをダウンロードし、実行してください。

### Web版（Pyodide / PyScript）
公開ページからそのまま利用できます。手元で確認したい場合は、各フォルダ内の `README.md` を参照してください（`.py` ファイルを `fetch` で読み込む都合上、`index.html` を直接開くのではなく、簡易サーバーを立てて確認する必要があります）。

```bash
cd webapp-pyodide   # または webapp-pyscript
python -m http.server 8000
```

`http://localhost:8000` にアクセスして確認します。

## 計算ロジックについて

PC版・Web版（Pyodide/PyScript）は、いずれも同じ計算ロジック（`calculator_manager.py` など）を使用しています。Tkinter依存部分（画面表示）のみ、各バージョンごとに実装が異なります。
