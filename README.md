# Fitbit Data Analyzer

FitbitのAPIを利用してユーザーのデータを取得・分析するためのPythonツールセットです。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fitbit-data-analyzer.streamlit.app)

## 機能

- Fitbit APIへの認証と認可
- アクセストークンの取得と更新
- 以下のデータ取得に対応:
  - ユーザープロファイル情報
  - アクティビティデータ（歩数、消費カロリーなど）
  - 睡眠データ
  - 心拍数データ
- Streamlitによる直感的なデータ可視化

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

## 使用方法

### 1. コマンドラインを使用する場合

新しい統合コマンドラインインターフェースを使用することで、簡単に各機能を実行できます。

#### アクセストークンの取得

初めてAPIを使用する場合は、認証コードからアクセストークンを取得する必要があります：

```bash
python3 main.py token --exchange
```

指示に従って認証プロセスを完了すると、アクセストークンとリフレッシュトークンが保存されます。

#### アクセストークンの更新

アクセストークンは約8時間で有効期限が切れます。更新するには：

```bash
python3 main.py token --refresh
```

#### データの取得

```bash
python3 main.py data [オプション]
```

オプション:
- `--date`: データを取得する日付（例: 2023-01-01、デフォルト: today）
- `--output-dir`: データを保存するディレクトリ（デフォルト: data）

#### データの処理

```bash
python3 main.py process [オプション]
```

オプション:
- `--input-dir`: 処理するデータのディレクトリ（デフォルト: data）
- `--output-dir`: 処理結果の保存先ディレクトリ（デフォルト: output）

### 2. Streamlitアプリを使用する場合

Streamlitアプリケーションを使って、インタラクティブなダッシュボードでデータを可視化できます：

```bash
streamlit run app.py
```

ブラウザで自動的にアプリが開き、以下の機能が利用できます：
- 歩数の推移グラフ（目標ライン付き）
- 睡眠時間の推移グラフ（推奨睡眠時間ゾーン付き）
- 安静時心拍数の推移グラフ
- 睡眠時間と翌日の歩数の相関分析

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

## 注意事項

- Fitbit APIは[レート制限](https://dev.fitbit.com/build/reference/web-api/developer-guide/application-design/#Rate-Limits)があります
- 個人的な使用を目的としており、商用利用する場合は[Fitbitの利用規約](https://dev.fitbit.com/build/reference/web-api/developer-guide/terms-of-service/)を確認してください

## ライセンス

MITライセンス


