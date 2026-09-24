# MT5 Close-All Gateway

A tiny stateless Flask service that lets a phone remotely arm a "close all
positions" flag, polled by an MT5 EA. See
`MT5_TradeAssistant/docs/superpowers/specs/2026-09-22-close-all-remote-gateway-design.md`
for the full design.

## Local development

    python -m venv venv
    source venv/Scripts/activate   # Windows Git Bash
    pip install -r requirements.txt
    PHONE_TOKEN=local-phone-token EA_TOKEN=local-ea-token python app.py

## Tests

    pytest -v

## Deploying to Render

1. Push this repo to GitHub.
2. In the Render dashboard: New -> Web Service -> connect this GitHub repo.
3. Runtime: Python 3. Build command: `pip install -r requirements.txt`.
   Start command: `gunicorn wsgi:app --workers 1` (already in `Procfile`,
   Render should detect it automatically).
4. Set environment variables `PHONE_TOKEN` and `EA_TOKEN` to two long random
   strings (e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   run twice). Keep them secret - `PHONE_TOKEN` goes in the bookmarked URL,
   `EA_TOKEN` goes into the MT5 EA's input parameter.
5. Deploy. Render's free tier sleeps after 15 minutes idle; the first
   request after that takes ~30-60s to wake it up. Upgrade to the paid
   Starter plan if that delay becomes annoying.
6. Bookmark `https://<your-app>.onrender.com/close-all?token=<PHONE_TOKEN>`
   on your phone.

## スマホのホーム画面に追加する方法

一度だけ、スマホのブラウザで `https://<your-app>.onrender.com/close-all?token=<PHONE_TOKEN>`
を開いてください。

**iOS (Safari):** 共有ボタン(四角から上矢印のアイコン)をタップ →
「ホーム画面に追加」を選択。

**Android (Chrome):** アドレスバー右側のメニュー(縦三点)をタップ →
「アプリをインストール」または「ホーム画面に追加」を選択。

以後はホーム画面に追加されたアイコンをタップするだけで、アドレスバーなしの
全画面表示でボタン画面が直接開きます。確認ダイアログは今まで通り表示されます。

**`PHONE_TOKEN` を変更(ローテーション)した場合:** 既にホーム画面に追加した
アイコンは古いトークンのURLを開こうとするため、タップしても白い画面や404
エラーが表示されるようになります。この場合はホーム画面のアイコンを削除し、
新しいトークンを含むURLで上記の手順をやり直して追加し直してください。トー
クンの変更に限らず、サーバーの起動待ちや一時的な通信エラーでも同じように
画面が固まって見えることがありますが、その場合は通常のブラウザでこのURL
を開く(=ブックマークから開く)だけで今まで通り操作できます。ホーム画面の
アイコンが開かなくなったときでも、通常のブックマークは常に避難経路として
使えます。

**セキュリティ上の注意:** ホーム画面のアイコンは、スマホのロックを解除した
状態で2回タップ(アイコン→確認ダイアログ)するだけで、口座内の全ポジション
を決済できる緊急スイッチです。スマホの画面ロック(生体認証・パスコード)は、
このツールの安全性の一部として必ず有効にしてください。
