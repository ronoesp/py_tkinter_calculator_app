# 電卓 Webアプリ（PyScript版）

前回作成したPyodide直接利用版と同じ電卓を、**PyScript**というフレームワークで書き直したものです。
計算ロジック本体（`calculator_manager.py` など）は前回から**一切変更していません**。

## Pyodide版との違い

| | Pyodide版 | PyScript版（このフォルダ） |
|---|---|---|
| `.py`ファイルの読み込み | JavaScriptで`fetch()`し、`pyodide.FS.writeFile()`で書き込む | `pyscript.json`の`"files"`設定に書くだけで自動的に配置される |
| DOM操作・イベント処理 | JavaScript側で記述 | `main.py`の中でPythonから直接記述（`from pyscript import document`） |
| 起動の仕組み | `<script>`内でJSからPyodideを手動ロード | `<script type="py" src="./main.py">`タグを置くだけ |
| 依存ファイル | なし（Pyodide本体のCDN読み込みのみ） | PyScriptのcore.js/core.cssを追加で読み込む |

`main.py`を見ると分かる通り、JavaScriptのコードが一切なくなり、全てPythonだけで完結しています。これがPyodideを直接使う場合との一番の違いです。

## ファイル構成

```
index.html            画面のHTML/CSS + PyScriptの起動タグ
pyscript.json         読み込む.pyファイルの設定
main.py               画面組み立て・イベント処理（元のcalculator_gui.py相当）
calculator_manager.py 計算ロジック（変更なし）
calculator_phase.py   同上
calculator_parameter.py 同上
calculator_system.py  同上
phase_handlers.py     同上
commons/
  __init__.py
  num_formatter.py    同上
```

## GitHub Pagesでの公開手順

Pyodide版と同じ手順です。

1. このフォルダの中身一式をGitHubリポジトリ直下に配置してコミット・プッシュします。
2. リポジトリの **Settings → Pages** を開きます。
3. Source を `Deploy from a branch`、Branch を `main`、フォルダを `/ (root)` に設定します。
4. `https://ユーザー名.github.io/リポジトリ名/` でアクセス可能になります。

## ローカルでの動作確認

Pyodide版と同様、`index.html`を直接ダブルクリックすると`.py`ファイルの読み込みに失敗するため、簡易サーバーを立てて確認してください。

```bash
python -m http.server 8000
```

その後ブラウザで `http://localhost:8000` を開きます。

## サーバー不要・競合の心配なし

Pyodide版と同じく、計算処理はすべて利用者のブラウザ内で完結し、サーバーへは一切通信しません。複数人が同時にアクセスしても、他の利用者と状態が競合することはありません。

## 補足：PyScriptのバージョンについて

`index.html`内で読み込んでいるPyScriptのバージョン（`https://pyscript.net/releases/2026.7.3/...`）は今後のリリースで変わる可能性があります。最新バージョンを使いたい場合は [pyscript.net](https://pyscript.net/) で最新のリリース番号を確認し、`core.css`・`core.js`のURL内のバージョン番号を置き換えてください。
