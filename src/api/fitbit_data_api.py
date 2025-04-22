#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FitbitのAPIを使用してユーザーのデータを取得するスクリプト
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import argparse
import traceback  # 追加: スタックトレースを出力するため

# .envファイルから環境変数を読み込む
load_dotenv()

def check_token_expiration():
    """トークンの有効期限を確認し、必要に応じて警告を表示する"""
    expiration_str = os.getenv("FITBIT_TOKEN_EXPIRATION")
    
    if not expiration_str:
        print("警告: トークンの有効期限情報が見つかりません")
        return True  # 変更: 有効期限がなくてもTrue（処理継続）を返す
    
    expiration_time = datetime.strptime(expiration_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    
    if now >= expiration_time:
        print("エラー: アクセストークンの有効期限が切れています")
        print("fitbit_token_refresh.pyを実行してトークンを更新してください")
        return False
    
    time_left = expiration_time - now
    if time_left.total_seconds() < 3600:  # 1時間未満
        print(f"警告: アクセストークンの有効期限まであと{int(time_left.total_seconds()/60)}分です")
        print("間もなくfitbit_token_refresh.pyを実行してトークンを更新してください")
    
    return True

def get_profile(access_token):
    """ユーザープロファイル情報を取得する"""
    url = "https://api.fitbit.com/1/user/-/profile.json"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:  # 追加: try-exceptでエラーをキャッチ
        print(f"APIリクエスト: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"エラー: プロファイル情報の取得に失敗しました (HTTP {response.status_code})")
            print(f"レスポンス: {response.text}")
            return None
        
        return response.json()
    except Exception as e:
        print(f"例外が発生しました: {str(e)}")
        traceback.print_exc()  # 追加: スタックトレースを出力
        return None

def get_activity_data(access_token, date="today"):
    """指定日のアクティビティデータを取得する"""
    url = f"https://api.fitbit.com/1/user/-/activities/date/{date}.json"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        print(f"APIリクエスト: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"エラー: アクティビティデータの取得に失敗しました (HTTP {response.status_code})")
            print(f"レスポンス: {response.text}")
            return None
        
        return response.json()
    except Exception as e:
        print(f"例外が発生しました: {str(e)}")
        traceback.print_exc()
        return None

def get_sleep_data(access_token, date="today"):
    """指定日の睡眠データを取得する"""
    url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        print(f"APIリクエスト: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"エラー: 睡眠データの取得に失敗しました (HTTP {response.status_code})")
            print(f"レスポンス: {response.text}")
            return None
        
        return response.json()
    except Exception as e:
        print(f"例外が発生しました: {str(e)}")
        traceback.print_exc()
        return None

def get_heart_rate_data(access_token, date="today"):
    """指定日の心拍数データを取得する"""
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{date}/1d.json"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        print(f"APIリクエスト: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"エラー: 心拍数データの取得に失敗しました (HTTP {response.status_code})")
            print(f"レスポンス: {response.text}")
            return None
        
        return response.json()
    except Exception as e:
        print(f"例外が発生しました: {str(e)}")
        traceback.print_exc()
        return None

def save_data_to_file(data, filename):
    """データをJSONファイルに保存する"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"データを{filename}に保存しました")

def get_date_range(end_date, days):
    """指定された終了日から指定された日数分の日付範囲を生成する"""
    if end_date == "today":
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = []
    
    for i in range(days):
        day = end_date_obj - timedelta(days=i)
        date_list.append(day.strftime("%Y-%m-%d"))
    
    return date_list

def main():
    parser = argparse.ArgumentParser(description="FitbitのAPIからデータを取得するスクリプト")
    parser.add_argument("--date", default="today", help="取得する日付（例: 2023-01-01、デフォルト: today）")
    parser.add_argument("--days", type=int, default=1, help="取得する日数（過去に遡る日数、デフォルト: 1）")
    parser.add_argument("--output-dir", default="data", help="データの保存先ディレクトリ（デフォルト: data）")
    args = parser.parse_args()
    
    print("=== Fitbit Data API Tool ===")
    
    # アクセストークンの取得と有効期限チェック
    access_token = os.getenv("FITBIT_ACCESS_TOKEN")
    if not access_token:
        print("エラー: FITBIT_ACCESS_TOKENが.envファイルにありません")
        print("fitbit_token_exchange.pyを実行してトークンを取得してください")
        return
    
    print(f"アクセストークン: {access_token[:10]}... (長さ: {len(access_token)}文字)")  # 追加: トークン情報を表示
    
    # トークンの有効期限チェック
    if not check_token_expiration():
        return
    
    try:  # 追加: 全体をtry-exceptで囲む
        # 出力ディレクトリの作成
        os.makedirs(args.output_dir, exist_ok=True)
        
        # ユーザープロファイルの取得
        print("\nユーザープロファイルを取得しています...")
        profile = get_profile(access_token)
        if profile:
            print(f"ユーザー情報: {profile['user']['fullName']} ({profile['user']['encodedId']})")
            save_data_to_file(profile, f"{args.output_dir}/profile.json")
        else:
            print("プロファイル情報の取得に失敗しました")
        
        # 日付範囲の取得
        date_range = get_date_range(args.date, args.days)
        print(f"\n{args.days}日分のデータを取得します（{date_range[0]}から{date_range[-1]}まで）")
        
        # 各日付のデータを取得
        for date in date_range:
            print(f"\n===== {date}のデータ取得 =====")
            
            # アクティビティデータの取得
            print("アクティビティデータを取得しています...")
            activity_data = get_activity_data(access_token, date)
            if activity_data:
                summary = activity_data.get("summary", {})
                steps = summary.get("steps", 0)
                print(f"歩数: {steps} 歩")
                save_data_to_file(activity_data, f"{args.output_dir}/activity_{date}.json")
            
            # 睡眠データの取得
            print("\n睡眠データを取得しています...")
            sleep_data = get_sleep_data(access_token, date)
            if sleep_data:
                if sleep_data.get("sleep"):
                    sleep_minutes = sum(item.get("minutesAsleep", 0) for item in sleep_data.get("sleep", []))
                    print(f"睡眠時間: {sleep_minutes//60}時間{sleep_minutes%60}分")
                else:
                    print("この日の睡眠データはありません")
                save_data_to_file(sleep_data, f"{args.output_dir}/sleep_{date}.json")
            
            # 心拍数データの取得
            print("\n心拍数データを取得しています...")
            heart_rate_data = get_heart_rate_data(access_token, date)
            if heart_rate_data:
                zones = heart_rate_data.get("activities-heart", [{}])[0].get("value", {}).get("heartRateZones", [])
                if zones:
                    resting_hr = heart_rate_data.get("activities-heart", [{}])[0].get("value", {}).get("restingHeartRate")
                    if resting_hr:
                        print(f"安静時心拍数: {resting_hr} bpm")
                    else:
                        print("この日の安静時心拍数データはありません")
                else:
                    print("この日の心拍数データはありません")
                save_data_to_file(heart_rate_data, f"{args.output_dir}/heart_rate_{date}.json")
        
        print("\n処理が完了しました！")
        print(f"すべてのデータは{args.output_dir}ディレクトリに保存されています")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {str(e)}")
        traceback.print_exc()  # 追加: スタックトレースを出力

if __name__ == "__main__":
    main() 