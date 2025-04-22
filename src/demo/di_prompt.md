
# 処理概要

Fitbitのデータセット`datasets/fitbit_data.csv`でデータ分析を実行し、可視化して。日本語で処理を行って。
Exploratory Data Analysis（探索的データ分析）を実施し、特徴量を作成して
疲労度や日々のパフォーマンス、がんばり度や健康度などの観点から分析して

## 描画について

描画は `workspace/titanic/demo_jp_font_visual.py` を参考にして日本語フォントでも文字化けしないようにして
FontPropertiesを使用して、set_themeのfontでフォントを指定して
グラフはseabornを使ってパステルカラーをテーマにしたおしゃれなグラフにして
グラフはoutputフォルダに保存して


`workspace/titanic/demo_jp_font_visual.py`

```python
from matplotlib.font_manager import FontProperties
font_path = "/usr/share/fonts/truetype/migmix/migmix-1p-regular.ttf"
font_prop = FontProperties(fname=font_path)
matplotlib.rcParams["font.family"] = font_prop.get_name()

# タイタニック号のサンプルデータを読み込む
df = sns.load_dataset('titanic')
# seabornのパステルカラーテーマを設定
sns.set_theme(style="whitegrid", palette="pastel", font=font_prop.get_name())
# 相関行列のヒートマップを描画
plt.figure(figsize=(10, 8))
sns.catplot(data=df, x='survived', y='class', kind='bar')
plt.title('特徴量間の相関')
plt.savefig("iris.png")
```


## 結論・考察

最後には結論や考察を実施して
疲労度や日々のパフォーマンス、がんばり度や健康度などの観点から結論や考察を実施して
考察の文章はoutputフォルダにConsideration.txtファイルで出力して
考察を導くために使用した数値データはConsideration.csvで出力して
結論の文章はoutputフォルダにconclusions.txtファイルで出力して
結論を導くために使用した数値データはoutputフォルダにconclusions.csvで出力して

