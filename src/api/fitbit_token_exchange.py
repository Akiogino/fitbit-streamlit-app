#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fitbitの認証コードを使ってアクセストークンを取得するスクリプト
"""

import os
import json
import requests
import base64
from dotenv import load_dotenv
import sys

# .envファイルから環境変数を読み込む
load_dotenv()

def get_tokens_from_code(code, client_id, client_secret, redirect_uri):
    """認証コードを使用してアクセストークンとリフレッシュトークンを取得する"""
    print("認証コードからトークンを取得しています...")
    
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
        "client_id": client_id,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code
    }
    
    response = requests.post("https://api.fitbit.com/oauth2/token", headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"エラー: トークンの取得に失敗しました (HTTP {response.status_code})")
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
    
    # .envファイルに書き込む
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("トークンを.envファイルに保存しました")

def main():
    print("=== Fitbit Token Exchange Tool ===")
    
    # 環境変数からクライアントIDとシークレットを取得
    client_id = os.getenv("FITBIT_CLIENT_ID")
    client_secret = os.getenv("FITBIT_CLIENT_SECRET")
    redirect_uri = os.getenv("FITBIT_REDIRECT_URI", "http://localhost:8080")
    
    if not client_id or not client_secret:
        print("エラー: FITBIT_CLIENT_IDとFITBIT_CLIENT_SECRETを.envファイルに設定してください")
        print("例: ")
        print("FITBIT_CLIENT_ID=your_client_id")
        print("FITBIT_CLIENT_SECRET=your_client_secret")
        return
    
    # コマンドライン引数から認証コードを取得するか、ユーザーに入力を求める
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        print("\n認証コードを入力してください。")
        print("注: このコードはFitbitの認証画面で「許可」をクリックした後、リダイレクトURLのcode=パラメータから取得できます。")
        code = input("認証コード: ").strip()
    
    # コードからトークンを取得
    tokens = get_tokens_from_code(code, client_id, client_secret, redirect_uri)
    
    if tokens:
        print("\nトークンの取得に成功しました！")
        print(f"アクセストークン: {tokens['access_token'][:20]}...")
        print(f"リフレッシュトークン: {tokens['refresh_token'][:20]}...")
        
        # トークンを.envファイルに保存
        save_tokens_to_env(tokens)
        
        print("\n次のステップ:")
        print("1. fitbit_data_api.pyを実行してFitbitデータを取得できます")
        print("2. アクセストークンの有効期間は通常8時間です")
        print("3. リフレッシュトークンを使用して新しいアクセストークンを取得できます")
    else:
        print("\nトークンの取得に失敗しました。以下を確認してください:")
        print("- 認証コードが正しいこと")
        print("- クライアントIDとシークレットが正しいこと")
        print("- リダイレクトURIがFitbitデベロッパーポータルの設定と一致していること")

if __name__ == "__main__":
    main() 