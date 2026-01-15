# line-notification-bot

Pythonで作った **LINE通知アプリ** です。  
**GitHub Actions** を使って、毎日決まった時間に **自動でLINEへメッセージを送信**します。

ローカルPCやサーバーは不要で、GitHub上だけで完結します。

---

## 概要
- 個人利用向けのシンプルなLINE通知ツール
- GitHub Actions による完全自動実行
- ローカル実行なし（クラウド完結）
- 環境変数は GitHub Secrets で安全に管理

---

## 機能
- LINE Messaging API を使ったメッセージ送信
- GitHub Actions による定期実行（cron）
- 手動実行（workflow_dispatch）対応
- concurrency による多重実行防止
- ログ出力あり（Actionsログで確認可能）

---

## 実行環境
- GitHub Actions（ubuntu-latest）
- Python 3.10
- LINE Messaging API（公式アカウント）

※ Windows / ローカルPCは使用しません

---

## 使用ライブラリ
- requests

---

## セットアップ

### 1. リポジトリを作成・clone
```bash
git clone https://github.com/your-name/line-notification-bot.git
cd line-notification-bot
