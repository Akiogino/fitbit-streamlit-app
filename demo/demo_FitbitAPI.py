import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from scipy.interpolate import interp1d
import seaborn as sns
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

# 設定ファイルのパス
CONFIG_FILE = "fitbit-token.json"
CLIENT_ID = "23RZLM"
CLIENT_SECRET = "263d767253671632e1fa7a61dea98564"

def load_config():
    """設定ファイルを読み込む"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"設定ファイル {CONFIG_FILE} が見つかりません。")
        exit(1)

def save_config(config):
    """設定ファイルを保存する"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def create_auth_header(access_token):
    """認証用のヘッダを作成する"""
    return {"Authorization": "Bearer " + access_token}

def refresh_access_token(config):
    """アクセストークンを更新する"""
    url = "https://api.fitbit.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": config["refresh_token"],
    }
    headers = {
        "Authorization": "Basic " + CLIENT_ID + ":" + CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=data, headers=headers)
    data = response.json()

    if "errors" in data:
        print(f"アクセストークンの更新に失敗しました: {data['errors'][0]['message']}")
        return False

    config["access_token"] = data["access_token"]
    config["refresh_token"] = data["refresh_token"]
    save_config(config)
    return True

def is_token_expired(response_data):
    """アクセストークンの有効期限が切れているかチェックする"""
    if "errors" in response_data:
        for error in response_data["errors"]:
            if error.get("errorType") == "expired_token":
                print("アクセストークンの有効期限が切れています。")
                return True
    return False

def make_api_request(url, headers):
    """APIリクエストを実行する"""
    response = requests.get(url, headers=headers)
    data = response.json()

    if is_token_expired(data):
        config = load_config()
        if refresh_access_token(config):
            headers = create_auth_header(config["access_token"])
            response = requests.get(url, headers=headers)
        else:
            print("アクセストークンの更新に失敗したため、リクエストを中止します。")
            exit(1)

    return response

def get_data(url, date):
    """指定されたURLとdateでデータを取得する"""
    config = load_config()
    headers = create_auth_header(config["access_token"])
    url = url.format(date=date)
    return make_api_request(url, headers)

def get_latest_csv_in_folder(folder_path, date_str):
    csv_files = [f for f in os.listdir(folder_path) if f.startswith(date_str) and f.endswith(".csv")]
    if not csv_files:
        return None
    latest_csv = max(csv_files)
    return os.path.join(folder_path, latest_csv)

def process_data(date):
    date_str = date.strftime("%Y-%m-%d")
    folder_path = f"Datasets/Day/{date_str}"
    os.makedirs(folder_path, exist_ok=True)

    latest_csv = get_latest_csv_in_folder(folder_path, date_str)
    if latest_csv:
        latest_data = pd.read_csv(latest_csv)
        latest_datetime = pd.to_datetime(latest_data['datetime'].max())
        if latest_datetime.time() >= pd.to_datetime('23:45').time():
            print(f"Skipping {date_str} data retrieval. Data already exists after 23:45.")
            return latest_data

    heart_rate_url = "https://api.fitbit.com/1/user/-/activities/heart/date/{date}/1d.json"
    spo2_url = "https://api.fitbit.com/1/user/-/spo2/date/{date}/all.json"
    sleep_url = "https://api.fitbit.com/1/user/-/sleep/date/{date}.json"

    response_heart = get_data(heart_rate_url, date_str)
    response_spo2 = get_data(spo2_url, date_str)
    response_sleep = get_data(sleep_url, date_str)

    data_heart = response_heart.json()
    data_spo2 = response_spo2.json()
    data_sleep = response_sleep.json()
    # print(data_sleep)

    df_spo2 = pd.DataFrame(data_spo2["minutes"])
    df_sleep = pd.DataFrame([{'dateTime': data['dateTime'], 'value': int(data['value'])} for data in data_sleep['sleep'][0]['minuteData']])
    df_heart = pd.DataFrame(data_heart["activities-heart-intraday"]["dataset"])

    df_spo2['datetime'] = pd.to_datetime(df_spo2['minute'])
    df_sleep['datetime'] = pd.to_datetime(date) + pd.to_timedelta(df_sleep['dateTime'])
    df_heart['datetime'] = pd.to_datetime(date) + pd.to_timedelta(df_heart['time'])

    df_spo2 = df_spo2[['datetime', 'value']]
    df_sleep = df_sleep[['datetime', 'value']]
    df_heart = df_heart[['datetime', 'value']]

    df_spo2.set_index('datetime', inplace=True)
    df_spo2 = df_spo2.resample('1min').mean()
    df_spo2['value'] = df_spo2['value'].interpolate(method='spline', order=2)

    df_sleep.set_index('datetime', inplace=True)
    df_sleep = df_sleep.resample('1min').interpolate(method='spline', order=2)

    df_heart.set_index('datetime', inplace=True)
    df_heart = df_heart.resample('1min').mean()
    df_heart['value'] = df_heart['value'].interpolate(method='spline', order=2)

    merged_data = pd.concat([df_spo2, df_sleep, df_heart], axis=1)
    merged_data.columns = ['spo2', 'sleep', 'heart_rate']
    merged_data = merged_data.reset_index()
    merged_data = merged_data.fillna(-1)

    os.makedirs(folder_path, exist_ok=True)
    merged_data.to_csv(f"{folder_path}/{date_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

    return merged_data

if __name__ == "__main__":

    start_date = datetime(2024, 3, 20)
    end_date = datetime(2024, 3, 23)
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # merged_data_list = []

    # for date in date_range:
    #     merged_data = process_data(date)
    #     if merged_data is not None:
    #         merged_data_list.append(merged_data)

    # final_merged_data = pd.concat(merged_data_list, ignore_index=True)
    # final_merged_data.to_csv('Datasets/fitbit_data.csv', index=False)


    final_merged_data = pd.read_csv('Datasets/fitbit_data.csv')
    print(final_merged_data.head())

    final_merged_data['datetime'] = final_merged_data['datetime'].astype(str)


    ###############################################
    # fig
    #
    # グラフのスタイルを設定
    sns.set(style="whitegrid")

    # Figure と Axes を作成
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # SpO2 のグラフをプロット
    sns.lineplot(x='datetime', y='spo2', data=final_merged_data, ax=axes[0])
    # axes[0].set_xticklabels([])
    axes[0].set_title('SpO2')
    axes[0].set_ylabel('SpO2 (%)')
    axes[0].xaxis.set_major_locator(mdates.HourLocator(interval = 10000))
    
    # 睡眠のグラフをプロット
    sns.lineplot(x='datetime', y='sleep', data=final_merged_data, ax=axes[1])
    axes[1].xaxis.set_major_locator(mdates.HourLocator(interval = 10000))
    axes[1].set_title('Sleep')
    axes[1].set_ylabel('Sleep Stage')

    # 心拍数のグラフをプロット
    sns.lineplot(x='datetime', y='heart_rate', data=final_merged_data, ax=axes[2])
    axes[2].xaxis.set_major_locator(mdates.HourLocator(interval = 10000))
    axes[2].set_title('Heart Rate')
    axes[2].set_ylabel('Heart Rate (bpm)')

    # x軸のラベルを45度回転
    plt.xticks(rotation=45)

    # ティックとラベルの間隔を調整
    plt.subplots_adjust(bottom=0.2)

    # グラフ間の間隔を調整
    plt.tight_layout()
    print("save.....")
    # グラフを表示
    plt.savefig('output/TOTAL-heart_rate-sleep-spo2.png')
    print("fin.....")