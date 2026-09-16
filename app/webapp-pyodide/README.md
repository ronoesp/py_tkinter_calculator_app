# 電卓 Webアプリ

Tkinter版電卓アプリを、サーバーを使わずブラウザだけで動くWebアプリに変換したものです。

## 仕組み

計算ロジック本体（以下のファイル）は元のコードから**一切変更していません**。

- `calculator_manager.py`
- `calculator_phase.py`
- `calculator_parameter.py`
- `calculator_system.py`
- `phase_handlers.py`
- `commons/num_formatter.py`

これらの `.py` ファイルを、[Pyodide](https://pyodide.org/)（PythonをWebAssemblyに変換してブラウザ内で実行する仕組み）を使って `index.html` から直接読み込み、実行しています。

Tkinterに依存していた `calculator_gui.py` / `gui_parts.py` / `gui_style.py` / `commons/vector2.py` の役割（画面の見た目・配置）だけを、`index.html` 内のHTML/CSS/JavaScriptに置き換えています。

## サーバー不要・競合の心配なし

- 計算処理は**すべて利用者のブラウザ内**で完結します（サーバーには一切通信しません）。
- そのため、複数人が同時にアクセスしても、他の利用者の入力や計算結果と混ざる・競合するといった問題は原理的に発生しません。
- 各利用者は、自分のブラウザの中だけで独立した電卓を操作していることになります。

## GitHub Pagesでの公開手順

1. このフォルダの中身一式（`index.html` と全ての `.py` ファイル、`commons` フォルダ）を、GitHubリポジトリの直下に配置してコミット・プッシュします。

   ```
   your-repo/
   ├── index.html
   ├── calculator_manager.py
   ├── calculator_phase.py
   ├── calculator_parameter.py
   ├── calculator_system.py
   ├── phase_handlers.py
   └── commons/
       ├── __init__.py
       └── num_formatter.py
   ```

2. GitHubのリポジトリページで **Settings → Pages** を開きます。
3. 「Build and deployment」の「Source」で `Deploy from a branch` を選択します。
4. Branch を `main`（または公開したいブランチ）、フォルダを `/ (root)` に設定して保存します。
5. しばらく待つと、`https://ユーザー名.github.io/リポジトリ名/` でアクセス可能になります。

## ローカルでの動作確認

`index.html` を直接ダブルクリックして開くと、ブラウザのセキュリティ制限（file://からのfetch禁止）によって `.py` ファイルの読み込みに失敗することがあります。ローカルで確認する場合は、簡易サーバーを立てて開いてください。

```bash
# このフォルダで実行
python -m http.server 8000
```

その後ブラウザで `http://localhost:8000` を開きます。

## 注意点

- 初回アクセス時、Pyodide本体（Python実行環境）の読み込みに数秒〜十数秒かかります（2回目以降はブラウザキャッシュにより速くなります）。
- `commons/__init__.py` は空ファイルですが、Pyodide上でパッケージとして正しく認識させるために必要なため追加しています。
