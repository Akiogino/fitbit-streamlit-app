import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    if gss_name == "GSpython":
        spreadsheet_key = GSS_TEMP_KEY

    #共有したスプレッドシートのキーを使ってシートの情報を取得
    worksheet = gs.open_by_key(spreadsheet_key).worksheet(gss_sheet_name)

    return worksheet

def main():
    # スプレッドシートを定義
    worksheet = get_gss_worksheet(gss_name='GSpython', gss_sheet_name='GSpython')

    # スプレッドシートを読み込み
    value = worksheet.acell("A1").value
    print(value)
    value = int(value) + 1

    # スプレッドシートを更新
    worksheet.update_acell("B1", value)

if __name__ == "__main__":
    # mainの実行
    main()