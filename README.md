# Fitbit データ分析ダッシュボード

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

Fitbitデータを可視化・分析するためのStreamlitアプリケーションです。

## 機能

- 歩数の推移グラフ（目標ライン付き）
- 睡眠時間の推移グラフ（推奨睡眠時間ゾーン付き）
- 安静時心拍数の推移グラフ
- 睡眠時間と翌日の歩数の相関分析

## 使用方法

### ローカルでの実行

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# アプリの実行
streamlit run app.py
```

### データの準備方法

1. Fitbitアカウントから[パーソナルデータをダウンロード](https://www.fitbit.com/settings/data/export)
2. ダウンロードしたZIPファイルをアプリにアップロード

または、ローカルにJSONファイルがある場合は、それらのパスを指定して読み込むこともできます。

## 注意事項

- このアプリはユーザーがアップロードしたデータを一時的に処理するだけで、データをサーバー上に保存しません。
- Fitbitデータの使用に関しては、[Fitbitの利用規約](https://www.fitbit.com/global/us/legal/terms-of-service)を確認してください。

## ディレクトリ構造

```
fitbit-di-python-analyzer/
├── src/                 # ソースコード
│   ├── api/             # Fitbit API関連のモジュール
│   ├── data/            # データ収集・処理のモジュール
│   ├── demo/            # デモンストレーション用のスクリプト
│   ├── utils/           # ユーティリティ関数
│   └── tests/           # テストコード
├── data/                # データ保存用ディレクトリ
│   └── raw/             # 生データ
├── output/              # 出力結果の保存先
├── docs/                # ドキュメント
├── notebook/            # Jupyter/Quartoノートブック
├── config/              # 設定ファイル
├── main.py              # メインエントリーポイント
├── app.py               # Streamlitアプリケーション
├── requirements.txt     # 依存パッケージ
├── Dockerfile           # Dockerイメージ定義
└── docker-compose.yml   # Docker Compose設定
```

## 初期設定

### 必要なもの

- Python 3.7以上
- Fitbit開発者アカウントとアプリの登録

### インストール方法

1. リポジトリをクローンまたはダウンロードします:

```bash
git clone https://github.com/yourusername/fitbit-di-python-analyzer.git
cd fitbit-di-python-analyzer
```

2. 必要なライブラリをインストールします:

```bash
pip3 install -r requirements.txt
```

3. `.env`ファイルを作成し、Fitbit APIの認証情報を設定します:

```
FITBIT_CLIENT_ID=あなたのクライアントID
FITBIT_CLIENT_SECRET=あなたのクライアントシークレット
```

## オンラインでの使用

このアプリは[Streamlit Cloud](https://fitbit-data-analyzer.streamlit.app)からアクセスすることもできます。

オンライン版の使用方法：
1. Fitbitからダウンロードしたデータをアップロード
2. グラフと分析結果をインタラクティブに閲覧
3. 表示期間の調整や統計データの確認

## Dockerを使った実行

Docker環境で実行することもできます：

```bash
docker-compose up -d
```

これにより、http://localhost:8501 でStreamlitアプリが利用可能になります。

## Fitbit開発者アカウントの設定

1. [Fitbit開発者サイト](https://dev.fitbit.com/)でアカウントを作成
2. 新しいアプリを登録
3. OAuth 2.0のアプリケーションタイプを「Personal」に設定
4. コールバックURLをアプリに設定（例: `http://localhost:8080/`）
5. 取得したクライアントIDとシークレットを`.env`ファイルに設定

## ライセンス

MITライセンス


