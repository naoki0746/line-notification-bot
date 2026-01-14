# line-notification-bot

Pythonで作ったLINE通知アプリです。  
Windowsのタスクスケジューラを使って、毎日決まった時間にLINEへメッセージを送信できます。

---

## 機能
- LINE Messaging API を使ってメッセージを送信
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
```text
requests
python-dotenv

## セットアップ
```bash
pip install -r requirements.txt
