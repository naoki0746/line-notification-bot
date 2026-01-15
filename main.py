# OSの環境変数を読むための標準ライブラリ
import os

# 例外が起きた時に「失敗として終了」するために使う標準ライブラリ
import sys

# 「今の時刻」や「待ち時間」などを扱う標準ライブラリ（ロックの有効期限計算に使う）
import time

# Pythonの辞書（dict）をJSON文字列に変換するための標準ライブラリ
import json

# ログ（動作記録）を見やすく出力するための標準ライブラリ
import logging

# ファイルパス操作をラクにする標準ライブラリ（ロックファイル作成に使う）
from pathlib import Path

# HTTP通信（API呼び出し）をする外部ライブラリ
import requests


# ----------------------------
# 必須環境変数を安全に取得する関数
# ----------------------------
def must_env(name: str) -> str:
    # 環境変数から name の値を読む（GitHub ActionsのSecretsは環境変数として渡される）
    v = os.getenv(name)

    # v が None や空文字なら「設定されていない」とみなす
    if not v:
        # どの環境変数が足りないか分かるようにエラー文を出して止める
        raise RuntimeError(f"Missing env var: {name}. Set it in GitHub Secrets.")

    # ちゃんと値があれば返す
    return v


# ----------------------------
# 多重起動防止（保険）
# - もし同時に2回動いたら二重送信になる可能性があるので防ぐ
# - GitHub Actionsでは concurrency で防ぐのが本命だが、念のためコードでもガードする
# ----------------------------
def acquire_lock(lock_path: str = ".run.lock", ttl_seconds: int = 60 * 30) -> None:
    # lock_path という文字列を Path オブジェクト（ファイル操作しやすい形）に変換
    p = Path(lock_path)

    # もしロックファイルがすでに存在していたら…
    if p.exists():
        # ファイルの最終更新時刻（mtime）から「今まで何秒たったか」を計算する
        age = time.time() - p.stat().st_mtime

        # age が ttl_seconds より小さい＝「最近作られたロック」＝まだ実行中かも
        if age < ttl_seconds:
            # ロックが有効なので処理を止める（多重実行防止）
            raise RuntimeError(f"Lock file exists: {lock_path} (age={int(age)}s). Aborting.")

        # TTLを超えて古いロックなら「前回異常終了」扱いにして消す
        p.unlink(missing_ok=True)

    # ロックファイルを作る（中身はプロセスID）
    p.write_text(str(os.getpid()), encoding="utf-8")


# ロック解除用（最後にロックファイルを削除する）
def release_lock(lock_path: str = ".run.lock") -> None:
    # ロックファイルがあれば削除（なくてもエラーにしない）
    Path(lock_path).unlink(missing_ok=True)


# ----------------------------
# LINEへPush送信（Messaging API）
# ----------------------------
def send_line_push_message(token: str, to: str, text: str) -> None:
    # LINE Messaging API の push メッセージ送信先URL
    url = "https://api.line.me/v2/bot/message/push"

    # HTTPヘッダー
    # Authorization: Bearer <アクセストークン>
    # Content-Type: JSON で送りますよ、という宣言
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # 送るデータ本体（JSONになる）
    # to: 送信先のID（userId / groupId / roomId）
    # messages: 送るメッセージの配列（今回はテキスト1件）
    payload = {
        "to": to,
        "messages": [{"type": "text", "text": text}],
    }

    # requests.post でHTTP POSTを送る
    # data=json.dumps(payload) で辞書 → JSON文字列へ変換して送る
    # timeout=20 は、20秒で応答がなければ止める（永遠に待たないため）
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)

    # 成功かどうか判定（2xxならOK）
    if not r.ok:
        # 失敗したらステータスコードと本文を出して止める（原因特定しやすい）
        raise RuntimeError(f"LINE API error: {r.status_code} {r.text}")


def main() -> None:
    # ログの基本設定
    # GitHub Actionsのログで見やすいように日時付きにする
    logging.basicConfig(
        level=logging.INFO,  # INFO以上を表示（DEBUGは出さない）
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # 実行開始時にロックを取る（多重実行防止）
    acquire_lock()

    # finally でロック解除したいので try/finally を使う
    try:
        # 必須の環境変数を取得（なければここでエラーになって止まる）
        token = must_env("LINE_CHANNEL_ACCESS_TOKEN")
        to = must_env("LINE_TO")

        # 送信するメッセージ本文を決める
        # もし LINE_MESSAGE という環境変数があればそれを使い、
        # なければ "定期通知です！" を使う
        message = os.getenv("LINE_MESSAGE", "定期通知です！")

        # ログ出力（何をするか分かる）
        logging.info("Sending LINE message...")

        # 実際にLINEへ送信
        send_line_push_message(token=token, to=to, text=message)

        # 成功ログ
        logging.info("Done.")

    finally:
        # 途中でエラーになっても必ずロック解除（次回実行できるように）
        release_lock()


# これは「このファイルが直接実行された時だけ main() を動かす」定番の書き方
# GitHub Actions では `python main.py` で実行するので、ここが動く
if __name__ == "__main__":
    try:
        # メイン処理実行
        main()
    except Exception as e:
        # 失敗した時はエラーを標準エラー出力へ出す（ログで赤く見えてわかりやすい）
        print(f"[ERROR] {e}", file=sys.stderr)

        # 終了コード1で終了（GitHub Actionsでジョブが失敗扱いになる）
        sys.exit(1)
