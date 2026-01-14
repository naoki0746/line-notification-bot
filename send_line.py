# dotenv というライブラリから load_dotenv 関数を読み込む
# .env ファイルを Python から使えるようにするための準備
from dotenv import load_dotenv

# .env ファイルを読み込んで、環境変数として有効化する
load_dotenv()


# OS（環境変数など）を扱うための標準ライブラリ
import os

# HTTP通信（API呼び出し）を行うための外部ライブラリ
import requests


# ----------------------------
# 環境変数を安全に取得する関数
# ----------------------------
def must_env(name: str) -> str:
    # 環境変数 name の値を取得する
    v = os.getenv(name)

    # もし値が存在しなかった場合（None や 空文字）
    if not v:
        # エラーを発生させてプログラムを止める
        raise RuntimeError(f"環境変数 {name} が設定されていません")

    # 正常に取得できた場合は、その値を返す
    return v


# LINEのチャネルアクセストークンを環境変数から取得
# （BotがLINEに命令を出すための鍵）
TOKEN = must_env("LINE_CHANNEL_ACCESS_TOKEN")

# メッセージの送信先（自分自身）の userId を環境変数から取得
USER_ID = must_env("LINE_USER_ID")


# ----------------------------
# LINEにテキストを送信する関数
# ----------------------------
def push_text(text: str) -> None:
    # LINE Messaging API の「Push Message」エンドポイントURL
    url = "https://api.line.me/v2/bot/message/push"

    # HTTPリクエストのヘッダー情報
    headers = {
        # 認証情報（Bearer トークン）
        "Authorization": f"Bearer {TOKEN}",

        # 送信するデータ形式は JSON であることを指定
        "Content-Type": "application/json",
    }

    # LINEに送るデータ本体（JSON）
    payload = {
        # メッセージの送信先（userId）
        "to": USER_ID,

        # 送信するメッセージの内容（今回はテキスト1件）
        "messages": [
            {
                "type": "text",  # メッセージの種類（テキスト）
                "text": text     # 実際に送信する文字列
            }
        ],
    }

    # POSTリクエストを送信して、LINE APIを呼び出す
    # timeout=10 は「10秒待って応答がなければ諦める」という意味
    r = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )

    # HTTPステータスコード（200なら成功）を表示
    print("status:", r.status_code)

    # LINE APIから返ってきたレスポンス内容を表示
    print(r.text)


# ----------------------------
# このファイルが直接実行されたときだけ動く処理
# ----------------------------
if __name__ == "__main__":
    # push_text 関数を呼び出して、テストメッセージを送信する
    push_text("テスト送信：自分のPCから送れた！")