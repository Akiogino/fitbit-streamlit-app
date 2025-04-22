FROM --platform=linux/arm64 python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    python3-dev \
    curl \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

# Quartoのインストール（arm64版）
RUN curl -LO https://quarto.org/download/latest/quarto-linux-arm64.deb && \
    gdebi --non-interactive quarto-linux-arm64.deb && \
    rm quarto-linux-arm64.deb

# Pythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 環境変数を設定
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# ポートを公開
EXPOSE 8000

# アプリケーションのコードをコピー
COPY . .

# Quartoでレンダリングを実行するコマンド
CMD ["quarto", "preview", "notebook/Fitbit_Demo_Sleep_visual.qmd", "--port", "8000", "--host", "0.0.0.0"] 