
<h1>
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/fitbit-python-analyzer/main/docs/icon.png" height=200px align="right"/>
fitbit-python-analyzer <br>
</h1>


Fitbit Python Analyzerは、Fitbitデバイスから収集された睡眠データと心拍数データを分析・可視化するためのPythonプロジェクトです。このプロジェクトは、自分の健康状態をより深く理解し、生活習慣の改善に役立てることを目的としています。


## 特徴

- Fitbit APIを使用して、睡眠データと心拍数データを取得
- 取得したデータをグラフで可視化
- 指定した期間のデータを取得・可視化可能
- 初心者にも分かりやすいJupyter Notebookでのコード解説
- Google Colabを使用しているため、環境構築が不要

## 内容

このリポジトリには、以下の3つのJupyter Notebookが含まれています。

1. [Fitbit_Demo[Sleep_visual]_python_fitbit.ipynb](notebook/Fitbit_Demo[Sleep_visual]_python_fitbit.ipynb)
   - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/108kwWcFWCppYo_35__JKvbosGiw6mv4D?usp=sharing)
   - Fitbitの睡眠データをグラフ化する方法を解説
   - プログラミングの知識がなくても、サンプルコードを実行するだけで簡単に可視化が可能
   - ![](https://raw.githubusercontent.com/Sunwood-ai-labs/fitbit-python-analyzer/main/docs/demo1.png)

2. [Fitbit_Demo[Heart_visual]_requests.ipynb](notebook/Fitbit_Demo[Heart_visual]_requests.ipynb)
   - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1UTlDbkUXhlw5wrwqovzEC-h7X9xZkQPw?usp=sharing)
   - Fitbit APIを使用して心拍数データを取得し、時系列グラフで可視化する方法を初心者向けに解説
   - ![](https://raw.githubusercontent.com/Sunwood-ai-labs/fitbit-python-analyzer/main/docs/demo2.png)

3. [Fitbit_Demo[Heart_visual_Range]_requests.ipynb](notebook/Fitbit_Demo[Heart_visual_Range]_requests.ipynb)
   - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12f3y4K5VFbpACMwxUM0k-c2q7QS7-VWi?usp=sharing)
   - 指定した期間のFitbit心拍数データを取得し、SeabornとMatplotlibを使ってグラフで可視化する方法を解説
   - ![](https://raw.githubusercontent.com/Sunwood-ai-labs/fitbit-python-analyzer/main/docs/demo3.png)
## 使い方

1. このリポジトリをクローンまたはダウンロードします。
2. 各Jupyter Notebookを開き、説明に従ってコードを実行します。
3. 必要に応じて、Fitbit APIの認証情報を設定します。
4. コードを実行し、生成されたグラフを確認します。

## 必要な環境

- Python 3.x
- Jupyter Notebook または Google Colab
- Fitbit API認証情報

## 貢献

このプロジェクトへの貢献を歓迎します。改善点やアイデアがある場合は、Issueを作成するかプルリクエストをお送りください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。