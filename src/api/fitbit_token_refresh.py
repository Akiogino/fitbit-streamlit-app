#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fitbitのリフレッシュトークンを使用して新しいアクセストークンを取得するスクリプト
"""

import os
import json
import requests
import base64
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .envファイルから環境変数を読み込む
load_dotenv()

def refresh_access_token(refresh_token, client_id, client_secret):
    """リフレッシュトークンを使用して新しいアクセストークンを取得する"""
    print("リフレッシュトークンから新しいアクセストークンを取得しています...")
    
    # Base64エンコードされた認証文字列を作成
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode("ascii")
    
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post("https://api.fitbit.com/oauth2/token", headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"エラー: トークンの更新に失敗しました (HTTP {response.status_code})")
        print(f"レスポンス: {response.text}")
        return None
    
    return response.json()

def save_tokens_to_env(tokens):
    """トークンを.envファイルに保存する"""
    print(".envファイルにトークンを保存しています...")
    
    env_file = ".env"
    env_vars = {}
    
    # 既存の.envファイルがあれば読み込む
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value
    
    # トークンを設定
    env_vars["FITBIT_ACCESS_TOKEN"] = tokens["access_token"]
    env_vars["FITBIT_REFRESH_TOKEN"] = tokens["refresh_token"]
    
    # 有効期限を計算して保存
    expires_in = tokens["expires_in"]
    expiration_time = datetime.now() + timedelta(seconds=expires_in)
    env_vars["FITBIT_TOKEN_EXPIRATION"] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # .envファイルに書き込む
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("トークンを.envファイルに保存しました")

def main():
    print("=== Fitbit Token Refresh Tool ===")
    
    # 環境変数からクライアントIDとシークレットを取得
    client_id = os.getenv("FITBIT_CLIENT_ID")
    client_secret = os.getenv("FITBIT_CLIENT_SECRET")
    refresh_token = os.getenv("FITBIT_REFRESH_TOKEN")
    
    if not client_id or not client_secret:
        print("エラー: FITBIT_CLIENT_IDとFITBIT_CLIENT_SECRETを.envファイルに設定してください")
        print("例: ")
        print("FITBIT_CLIENT_ID=your_client_id")
        print("FITBIT_CLIENT_SECRET=your_client_secret")
        return
    
    if not refresh_token:
        print("エラー: FITBIT_REFRESH_TOKENが.envファイルにありません")
        print("先に認証コードを使用してトークンを取得してください（fitbit_token_exchange.pyを実行）")
        return
    
    # リフレッシュトークンからアクセストークンを取得
    tokens = refresh_access_token(refresh_token, client_id, client_secret)
    
    if tokens:
        print("\nトークンの更新に成功しました！")
        print(f"新しいアクセストークン: {tokens['access_token'][:20]}...")
        print(f"新しいリフレッシュトークン: {tokens['refresh_token'][:20]}...")
        print(f"有効期間: {tokens['expires_in']} 秒（約 {tokens['expires_in']//3600} 時間）")
        
        # トークンを.envファイルに保存
        save_tokens_to_env(tokens)
        
        print("\n次のステップ:")
        print("1. fitbit_data_api.pyを実行してFitbitデータを取得できます")
        print("2. アクセストークンの有効期間は通常8時間です")
    else:
        print("\nトークンの更新に失敗しました。以下を確認してください:")
        print("- リフレッシュトークンが正しいこと")
        print("- クライアントIDとシークレットが正しいこと")
        print("- Fitbitアカウントが有効であること")

if __name__ == "__main__":
    main() 