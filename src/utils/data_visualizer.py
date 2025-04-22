#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitbitデータを可視化するスクリプト
Plotlyを使用して過去30日分のデータをグラフ化する
"""

import os
import json
import glob
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import argparse
from datetime import datetime

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
            
            # データを追加
            data.append({
                'date': date,
                'steps': steps
            })
        except Exception as e:
            print(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
    
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
            
            # データを追加
            data.append({
                'date': date,
                'sleep_hours': sleep_hours
            })
        except Exception as e:
            print(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
    
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
            print(f"Warning: {file}の読み込み中にエラーが発生しました: {e}")
    
    # DataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('date')
    
    return df

def create_visualizations(activity_df, sleep_df, heart_rate_df, output_dir):
    """データを可視化してグラフを保存する"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 日付を文字列に変換（グラフ表示用）
    if not activity_df.empty:
        activity_df['date_str'] = activity_df['date'].dt.strftime('%Y-%m-%d')
    if not sleep_df.empty:
        sleep_df['date_str'] = sleep_df['date'].dt.strftime('%Y-%m-%d')
    if not heart_rate_df.empty:
        heart_rate_df['date_str'] = heart_rate_df['date'].dt.strftime('%Y-%m-%d')
    
    # 1. 歩数の可視化
    if not activity_df.empty:
        fig_steps = px.bar(
            activity_df, 
            x='date_str', 
            y='steps',
            title='過去30日間の歩数',
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
        fig_steps.write_html(os.path.join(output_dir, 'daily_steps.html'))
    
    # 2. 睡眠時間の可視化
    if not sleep_df.empty:
        fig_sleep = px.bar(
            sleep_df, 
            x='date_str', 
            y='sleep_hours',
            title='過去30日間の睡眠時間',
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
        fig_sleep.write_html(os.path.join(output_dir, 'daily_sleep.html'))
    
    # 3. 安静時心拍数の可視化
    if not heart_rate_df.empty:
        fig_hr = px.line(
            heart_rate_df, 
            x='date_str', 
            y='resting_heart_rate',
            title='過去30日間の安静時心拍数',
            labels={'date_str': '日付', 'resting_heart_rate': '安静時心拍数 (bpm)'},
            markers=True
        )
        fig_hr.update_layout(
            xaxis_title='日付',
            yaxis_title='安静時心拍数 (bpm)',
            xaxis={'categoryorder': 'category ascending'},
            yaxis={'rangemode': 'tozero'}
        )
        fig_hr.write_html(os.path.join(output_dir, 'daily_heart_rate.html'))
    
    # 4. 総合ダッシュボード
    # 3つのグラフを組み合わせた総合グラフを作成
    fig_combined = make_subplots(
        rows=3, cols=1,
        subplot_titles=('歩数', '睡眠時間 (時間)', '安静時心拍数 (bpm)'),
        vertical_spacing=0.1
    )
    
    # 歩数のグラフを追加
    if not activity_df.empty:
        fig_combined.add_trace(
            go.Bar(
                x=activity_df['date_str'], 
                y=activity_df['steps'],
                name='歩数',
                marker_color='purple'
            ),
            row=1, col=1
        )
        # 目標歩数（10,000歩）の線を追加
        fig_combined.add_shape(type="line",
            xref="x", yref="y",
            x0=activity_df['date_str'].iloc[0], y0=10000, 
            x1=activity_df['date_str'].iloc[-1], y1=10000,
            line=dict(color="red", width=2, dash="dash"),
            row=1, col=1
        )
    
    # 睡眠時間のグラフを追加
    if not sleep_df.empty:
        fig_combined.add_trace(
            go.Bar(
                x=sleep_df['date_str'], 
                y=sleep_df['sleep_hours'],
                name='睡眠時間',
                marker_color='blue'
            ),
            row=2, col=1
        )
        # 推奨睡眠時間（7-9時間）のゾーンを追加
        fig_combined.add_shape(type="rect",
            xref="x2", yref="y2",
            x0=sleep_df['date_str'].iloc[0], y0=7, 
            x1=sleep_df['date_str'].iloc[-1], y1=9,
            fillcolor="rgba(0,255,0,0.2)",
            line_width=0,
            row=2, col=1
        )
    
    # 心拍数のグラフを追加
    if not heart_rate_df.empty:
        fig_combined.add_trace(
            go.Scatter(
                x=heart_rate_df['date_str'], 
                y=heart_rate_df['resting_heart_rate'],
                name='安静時心拍数',
                mode='lines+markers',
                line=dict(color='green')
            ),
            row=3, col=1
        )
    
    # レイアウトを設定
    fig_combined.update_layout(
        title_text='Fitbit データ 過去30日間のサマリー',
        height=900,
        showlegend=False
    )
    
    # X軸ラベルを設定
    fig_combined.update_xaxes(title_text='日付', row=3, col=1)
    
    # Y軸ラベルを設定
    fig_combined.update_yaxes(title_text='歩数', row=1, col=1)
    fig_combined.update_yaxes(title_text='睡眠時間 (時間)', row=2, col=1)
    fig_combined.update_yaxes(title_text='心拍数 (bpm)', row=3, col=1)
    
    # 総合グラフを保存
    fig_combined.write_html(os.path.join(output_dir, 'fitbit_dashboard.html'))
    
    # 5. 相関分析グラフ
    # 睡眠時間と次の日の歩数の相関
    if not sleep_df.empty and not activity_df.empty:
        # データフレームをマージ
        sleep_df['next_day'] = sleep_df['date'] + pd.Timedelta(days=1)
        merged_df = pd.merge(
            sleep_df, 
            activity_df,
            left_on='next_day',
            right_on='date',
            suffixes=('_sleep', '_steps')
        )
        
        if not merged_df.empty:
            fig_corr = px.scatter(
                merged_df, 
                x='sleep_hours', 
                y='steps',
                title='睡眠時間と翌日の歩数の関係',
                labels={
                    'sleep_hours': '睡眠時間 (時間)', 
                    'steps': '翌日の歩数'
                },
                trendline='ols',
                trendline_color_override='red'
            )
            
            fig_corr.update_layout(
                xaxis_title='睡眠時間 (時間)',
                yaxis_title='翌日の歩数',
                xaxis={'rangemode': 'tozero'},
                yaxis={'rangemode': 'tozero'}
            )
            
            fig_corr.write_html(os.path.join(output_dir, 'sleep_steps_correlation.html'))
    
    print(f"可視化が完了しました。グラフは {output_dir} ディレクトリに保存されています。")

def main():
    parser = argparse.ArgumentParser(description="Fitbitデータを可視化するスクリプト")
    parser.add_argument("--input-dir", default="data", help="入力データのディレクトリ（デフォルト: data）")
    parser.add_argument("--output-dir", default="output/visualization", help="出力グラフの保存先ディレクトリ（デフォルト: output/visualization）")
    args = parser.parse_args()
    
    print("=== Fitbit Data Visualizer ===")
    
    # 各種データをロード
    print("\nアクティビティデータをロードしています...")
    activity_df = load_activity_data(args.input_dir)
    print(f"{len(activity_df)}日分のアクティビティデータをロードしました")
    
    print("\n睡眠データをロードしています...")
    sleep_df = load_sleep_data(args.input_dir)
    print(f"{len(sleep_df)}日分の睡眠データをロードしました")
    
    print("\n心拍数データをロードしています...")
    heart_rate_df = load_heart_rate_data(args.input_dir)
    print(f"{len(heart_rate_df)}日分の心拍数データをロードしました")
    
    # 可視化を作成
    print("\nデータの可視化を行っています...")
    create_visualizations(activity_df, sleep_df, heart_rate_df, args.output_dir)

if __name__ == "__main__":
    main() 