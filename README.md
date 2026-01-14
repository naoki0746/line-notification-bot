# line-notification-bot

Pythonで作った **LINE通知アプリ** です。  
Windowsのタスクスケジューラを使って、**毎日決まった時間にLINEへメッセージを送信**できます。

---

## 概要
- 個人利用向けのシンプルなLINE通知ツール
- サーバー不要（Windows PCで動作）
- タスクスケジューラと組み合わせて定期実行可能

---

## 機能
- LINE Messaging API を使ったメッセージ送信
- タスクスケジューラ対応（1日1回送信）
- 多重起動防止ガードあり
- ログ出力あり

---

## 動作環境
- Windows 10 / 11
- Python 3.10
- LINE Messaging API（公式アカウント）

---

## 使用ライブラリ
- requests
- python-dotenv

---

## セットアップ
```bash
pip install -r requirements.txt
