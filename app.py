#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitbitデータを可視化するStreamlitアプリ
"""

import os
import json
import glob
import tempfile
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import zipfile
import io
import numpy as np

# ページ設定
st.set_page_config(
    page_title="Fitbit データ分析ダッシュボード",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトルとヘッダー
st.title("Fitbit データ分析ダッシュボード")
st.markdown("### 健康データの可視化・分析ツール")

# サイドバー
st.sidebar.header("設定")

# データソース選択
data_source = st.sidebar.radio(
    "データソース",
    ["デモデータ", "ローカルフォルダ", "ZIPファイルをアップロード"],
    index=0
)

# データディレクトリ設定
if data_source == "デモデータ":
    data_dir = "sample_data"
    st.sidebar.info("デモデータを使用しています。実際のFitbitデータをアップロードすることもできます。")
elif data_source == "ローカルフォルダ":
    data_dir = st.sidebar.text_input("データディレクトリ", value="data")
else:
    # ZIPファイルのアップロード
    uploaded_file = st.sidebar.file_uploader("Fitbitデータのzipファイルをアップロード", type=["zip"])
    if uploaded_file is not None:
        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            # ZIPファイルを読み込み
            z = zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue()))
            # すべてのファイルを一時ディレクトリに展開
            z.extractall(temp_dir)
            # 一時ディレクトリをデータディレクトリとして使用
            data_dir = temp_dir
    else:
        st.sidebar.warning("ZIPファイルをアップロードしてください")
        # デモデータを使用するオプション
        use_demo_data = st.sidebar.checkbox("デモデータを使用", value=True)
        if use_demo_data:
            data_dir = "sample_data"  # デモデータディレクトリ
        else:
            st.warning("データがアップロードされていません。ZIPファイルをアップロードするか、デモデータを使用してください。")
            st.stop()

# 表示設定
days_to_show = st.sidebar.slider("表示する日数", min_value=7, max_value=90, value=30)

# データロード関数
def load_activity_data(data_dir):
    """アクティビティデータをロードしてDataFrameに変換する"""
    files = glob.glob(os.path.join(data_dir, "activity_*.json"))
    data = []
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
            # ファイル名から日付を抽出
            date_str = os.path.basename(file).replace('activity_', '').replace('.json', '')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # サマリーから歩数を取得
            steps = content.get('summary', {}).get('steps', 0)
            
            # 活動カロリー
            active_calories = content.get('summary', {}).get('activityCalories', 0)
            
            # データを追加
            data.append({
                'date': date,
                'steps': steps,
                'active_calories': active_calories
            })
        except Exception as e:
            st.warning(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
        # 最新のdays_to_show日間のデータに制限
        if len(df) > days_to_show:
            df = df.tail(days_to_show)
    
    return df

def load_sleep_data(data_dir):
    """睡眠データをロードしてDataFrameに変換する"""
    files = glob.glob(os.path.join(data_dir, "sleep_*.json"))
    data = []
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # ファイル名から日付を抽出
            date_str = os.path.basename(file).replace('sleep_', '').replace('.json', '')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # 睡眠時間（分）を計算
            sleep_minutes = 0
            if 'sleep' in content and content['sleep']:
                sleep_minutes = sum(item.get('minutesAsleep', 0) for item in content['sleep'])
            
            # 睡眠時間（時間）に変換
            sleep_hours = sleep_minutes / 60
            
            # 睡眠効率
            efficiency = 0
            if 'sleep' in content and content['sleep']:
                efficiency_values = [item.get('efficiency', 0) for item in content['sleep']]
                if efficiency_values:
                    efficiency = sum(efficiency_values) / len(efficiency_values)
            
            # データを追加
            data.append({
                'date': date,
                'sleep_hours': sleep_hours,
                'efficiency': efficiency
            })
        except Exception as e:
            st.warning(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
        # 最新のdays_to_show日間のデータに制限
        if len(df) > days_to_show:
            df = df.tail(days_to_show)
    
    return df

def load_heart_rate_data(data_dir):
    """心拍数データをロードしてDataFrameに変換する"""
    files = glob.glob(os.path.join(data_dir, "heart_rate_*.json"))
    data = []
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # ファイル名から日付を抽出
            date_str = os.path.basename(file).replace('heart_rate_', '').replace('.json', '')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # 安静時心拍数を取得
            resting_hr = None
            if 'activities-heart' in content and content['activities-heart']:
                resting_hr = content['activities-heart'][0].get('value', {}).get('restingHeartRate')
            
            # データを追加
            if resting_hr is not None:
                data.append({
                    'date': date,
                    'resting_heart_rate': resting_hr
                })
        except Exception as e:
            st.warning(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
        # 最新のdays_to_show日間のデータに制限
        if len(df) > days_to_show:
            df = df.tail(days_to_show)
    
    return df

# アプリの説明
with st.expander("このアプリについて"):
    st.markdown("""
    ### Fitbit データ分析ダッシュボードとは？
    
    このアプリは、Fitbitから取得したデータを視覚化・分析するためのツールです。以下の機能があります：
    
    1. **歩数の推移**: 日々の歩数を確認し、目標（10,000歩）との比較ができます
    2. **睡眠時間の推移**: 睡眠時間をグラフ化し、推奨睡眠時間（7-9時間）との比較ができます
    3. **心拍数の推移**: 安静時心拍数の変化を追跡できます
    4. **相関分析**: 睡眠時間と翌日の歩数の関係性を分析できます
    
    ### データの準備方法
    
    1. Fitbitアカウントから[パーソナルデータをダウンロード](https://www.fitbit.com/settings/data/export)
    2. ダウンロードしたZIPファイルをこのアプリにアップロード
    
    または、ローカルにJSONファイルがある場合は、それらのパスを指定して読み込むこともできます。
    """)

# データ読み込み状態を表示
with st.spinner('データを読み込んでいます...'):
    activity_df = load_activity_data(data_dir)
    sleep_df = load_sleep_data(data_dir)
    heart_rate_df = load_heart_rate_data(data_dir)

# データの有無をチェック
if activity_df.empty and sleep_df.empty and heart_rate_df.empty:
    st.error(f"指定されたディレクトリ '{data_dir}' にデータが見つかりませんでした。正しいZIPファイルをアップロードするか、有効なデータディレクトリを指定してください。")
    st.markdown("""
    ### データが見つかりませんでした
    
    以下を確認してください：
    
    1. アップロードしたZIPファイルに正しいFitbitデータが含まれているか
    2. ローカルフォルダを指定した場合、そのフォルダに `activity_*.json`、`sleep_*.json`、`heart_rate_*.json` 形式のファイルが含まれているか
    
    #### Fitbitからデータをエクスポートする方法
    
    1. [Fitbitウェブサイト](https://www.fitbit.com)にログイン
    2. 右上のユーザーアイコンをクリック
    3. 「アカウント設定」→「データのエクスポート」を選択
    4. 「アカウントデータをリクエスト」をクリックし、手順に従う
    """)
    st.stop()

# データの基本情報
st.subheader("データの概要")
col1, col2, col3 = st.columns(3)

with col1:
    if not activity_df.empty:
        avg_steps = int(activity_df['steps'].mean())
        st.metric("1日の平均歩数", f"{avg_steps:,} 歩", delta=None)
    else:
        st.metric("1日の平均歩数", "データなし", delta=None)

with col2:
    if not sleep_df.empty:
        avg_sleep = round(sleep_df['sleep_hours'].mean(), 1)
        st.metric("1日の平均睡眠時間", f"{avg_sleep} 時間", delta=None)
    else:
        st.metric("1日の平均睡眠時間", "データなし", delta=None)

with col3:
    if not heart_rate_df.empty:
        avg_hr = int(heart_rate_df['resting_heart_rate'].mean())
        st.metric("平均安静時心拍数", f"{avg_hr} bpm", delta=None)
    else:
        st.metric("平均安静時心拍数", "データなし", delta=None)

# タブでコンテンツを整理
tab1, tab2, tab3 = st.tabs(["歩数", "睡眠", "心拍数"])

# タブ1: 歩数データ
with tab1:
    if not activity_df.empty:
        st.subheader("歩数の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        activity_df['date_str'] = activity_df['date'].dt.strftime('%Y-%m-%d')
        
        # 歩数グラフ
        fig_steps = px.bar(
            activity_df, 
            x='date_str', 
            y='steps',
            title='歩数の推移',
            labels={'date_str': '日付', 'steps': '歩数'},
            color='steps',
            color_continuous_scale='Viridis'
        )
        
        fig_steps.update_layout(
            xaxis_title='日付',
            yaxis_title='歩数',
            xaxis={'categoryorder': 'category ascending'},
            yaxis={'rangemode': 'tozero'}
        )
        
        # 目標歩数（10,000歩）の線を追加
        fig_steps.add_shape(type="line",
            xref="paper", yref="y",
            x0=0, y0=10000, x1=1, y1=10000,
            line=dict(color="red", width=2, dash="dash")
        )
        
        fig_steps.add_annotation(
            x=0.5, y=10000,
            xref="paper", yref="y",
            text="目標: 10,000歩",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )
        
        st.plotly_chart(fig_steps, use_container_width=True)
        
        # 統計情報
        st.subheader("歩数の統計")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最大歩数", f"{int(activity_df['steps'].max()):,} 歩", delta=None)
        with col2:
            st.metric("最小歩数", f"{int(activity_df['steps'].min()):,} 歩", delta=None)
        with col3:
            days_over_10k = len(activity_df[activity_df['steps'] >= 10000])
            st.metric("目標達成日数", f"{days_over_10k} 日", delta=None)
    else:
        st.info("歩数データがありません")

# タブ2: 睡眠データ
with tab2:
    if not sleep_df.empty:
        st.subheader("睡眠時間の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        sleep_df['date_str'] = sleep_df['date'].dt.strftime('%Y-%m-%d')
        
        # 睡眠時間グラフ
        fig_sleep = px.bar(
            sleep_df, 
            x='date_str', 
            y='sleep_hours',
            title='睡眠時間の推移',
            labels={'date_str': '日付', 'sleep_hours': '睡眠時間 (時間)'},
            color='sleep_hours',
            color_continuous_scale='Turbo'
        )
        
        fig_sleep.update_layout(
            xaxis_title='日付',
            yaxis_title='睡眠時間 (時間)',
            xaxis={'categoryorder': 'category ascending'},
            yaxis={'rangemode': 'tozero'}
        )
        
        # 推奨睡眠時間（7-9時間）のゾーンを追加
        fig_sleep.add_shape(type="rect",
            xref="paper", yref="y",
            x0=0, y0=7, x1=1, y1=9,
            fillcolor="rgba(0,255,0,0.2)",
            line_width=0
        )
        
        fig_sleep.add_annotation(
            x=0.5, y=8,
            xref="paper", yref="y",
            text="推奨睡眠時間: 7-9時間",
            showarrow=False,
            font=dict(color="green")
        )
        
        st.plotly_chart(fig_sleep, use_container_width=True)
        
        # 統計情報
        st.subheader("睡眠の統計")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最大睡眠時間", f"{round(sleep_df['sleep_hours'].max(), 1)} 時間", delta=None)
        with col2:
            st.metric("最小睡眠時間", f"{round(sleep_df['sleep_hours'].min(), 1)} 時間", delta=None)
        with col3:
            days_good_sleep = len(sleep_df[(sleep_df['sleep_hours'] >= 7) & (sleep_df['sleep_hours'] <= 9)])
            st.metric("推奨時間内の日数", f"{days_good_sleep} 日", delta=None)
    else:
        st.info("睡眠データがありません")

# タブ3: 心拍数データ
with tab3:
    if not heart_rate_df.empty:
        st.subheader("安静時心拍数の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        heart_rate_df['date_str'] = heart_rate_df['date'].dt.strftime('%Y-%m-%d')
        
        # 心拍数グラフ
        fig_hr = px.line(
            heart_rate_df, 
            x='date_str', 
            y='resting_heart_rate',
            title='安静時心拍数の推移',
            labels={'date_str': '日付', 'resting_heart_rate': '安静時心拍数 (bpm)'},
            markers=True
        )
        
        fig_hr.update_layout(
            xaxis_title='日付',
            yaxis_title='安静時心拍数 (bpm)',
            xaxis={'categoryorder': 'category ascending'},
            yaxis={'rangemode': 'tozero'}
        )
        
        st.plotly_chart(fig_hr, use_container_width=True)
        
        # 統計情報
        st.subheader("心拍数の統計")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最高安静時心拍数", f"{int(heart_rate_df['resting_heart_rate'].max())} bpm", delta=None)
        with col2:
            st.metric("最低安静時心拍数", f"{int(heart_rate_df['resting_heart_rate'].min())} bpm", delta=None)
        with col3:
            hr_trend = int(heart_rate_df['resting_heart_rate'].iloc[-1] - heart_rate_df['resting_heart_rate'].iloc[0])
            delta_color = "inverse" if hr_trend < 0 else "normal"
            st.metric("期間中の変化", f"{abs(hr_trend)} bpm", delta=f"{hr_trend} bpm", delta_color=delta_color)
    else:
        st.info("心拍数データがありません")

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>このアプリはFitbitデータを可視化するためのオープンソースツールです。</p>
    <p><a href="https://github.com/yourusername/fitbit-di-python-analyzer" target="_blank">GitHub</a>でソースコードを確認できます。</p>
</div>
""", unsafe_allow_html=True)

st.caption("© 2024 Fitbit Data Analyzer") 