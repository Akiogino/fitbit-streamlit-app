import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# 環境変数の設定
GSS_TEMP_KEY = "19oFmx87RiQvkeodOPptUy6FGqfB_FdMns9cW9QXuYx0"

# worksheetの情報を返す関数
def get_gss_worksheet(gss_name, gss_sheet_name):
    #jsonファイルを使って認証情報を取得
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    c = ServiceAccountCredentials.from_json_keyfile_name('makidemodrive-8f2f32d3daec.json', scope)
    #認証情報を使ってスプレッドシートの操作権を取得
    gs = gspread.authorize(c)
    # スプレッドシート名をもとに、キーを設定
    if gss_name == "FitbitSummary":
        spreadsheet_key = GSS_TEMP_KEY
    #共有したスプレッドシートのキーを使ってシートの情報を取得
    worksheet = gs.open_by_key(spreadsheet_key).worksheet(gss_sheet_name)
    return worksheet

def append_to_sheet(worksheet, file_paths):
    today = date.today().strftime("%Y-%m-%d")  # 今日の日付を文字列形式で取得
    row_data = [today]  # 日付を最初の要素として追加

    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            row_data.append(content)
        else:
            row_data.append("")
    
    # スプレッドシートの最終行に内容を追記
    worksheet.append_row(row_data, value_input_option='USER_ENTERED', insert_data_option="INSERT_ROWS")

def make_api_request(url, prompt_file):
    # マークダウンファイルからDI_PROMPTを読み込む
    with open(prompt_file, "r", encoding="utf-8") as file:
        DI_PROMPT = file.read()

    payload = {"text": DI_PROMPT}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()["result"]
        print(result)
        print("----------------------------------------")
        return True
    else:
        print(f"Request failed with status code {response.status_code}")
        return False

def main():
    url = "http://localhost:8000/data-visualization"
    prompt_file = "demo/di_prompt.md"

    # APIリクエストを送信
    success = make_api_request(url, prompt_file)

    if success:
        # スプレッドシートを定義
        worksheet = get_gss_worksheet(gss_name='FitbitSummary', gss_sheet_name='FitbitSummary')

        # 追記するファイルのパスをリストで指定
        file_paths = [
            "output/Consideration.txt",
            "output/Consideration.csv",
            "output/conclusions.txt",
            "output/conclusions.csv",
        ]
        
        # ファイルの内容を横に並べてスプレッドシートに追記
        append_to_sheet(worksheet, file_paths)

if __name__ == "__main__":
    # mainの実行
    main()