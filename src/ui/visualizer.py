#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitbitデータの可視化機能を提供するモジュール
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class FitbitVisualizer:
    """Fitbitデータの可視化を行うクラス"""
    
    def __init__(self):
        """初期化"""
        pass
    
    def show_steps_chart(self, activity_df):
        """歩数のグラフを表示
        
        Parameters:
        -----------
        activity_df : pd.DataFrame
            アクティビティデータ（歩数を含むDataFrame）
        """
        if activity_df.empty:
            st.info("歩数データがありません")
            return
        
        st.subheader("歩数の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        activity_df = activity_df.copy()
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
        fig_steps.add_shape(
            type="line",
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
    
    def show_sleep_chart(self, sleep_df):
        """睡眠時間のグラフを表示
        
        Parameters:
        -----------
        sleep_df : pd.DataFrame
            睡眠データ（睡眠時間を含むDataFrame）
        """
        if sleep_df.empty:
            st.info("睡眠データがありません")
            return
        
        st.subheader("睡眠時間の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        sleep_df = sleep_df.copy()
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
        fig_sleep.add_shape(
            type="rect",
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
    
    def show_heart_rate_chart(self, heart_rate_df):
        """心拍数のグラフを表示
        
        Parameters:
        -----------
        heart_rate_df : pd.DataFrame
            心拍数データ（安静時心拍数を含むDataFrame）
        """
        if heart_rate_df.empty:
            st.info("心拍数データがありません")
            return
        
        st.subheader("安静時心拍数の推移")
        
        # 日付を文字列に変換（グラフ表示用）
        heart_rate_df = heart_rate_df.copy()
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
    
    def show_data_summary(self, activity_df, sleep_df, heart_rate_df):
        """データの概要を表示
        
        Parameters:
        -----------
        activity_df : pd.DataFrame
            アクティビティデータ
        sleep_df : pd.DataFrame
            睡眠データ
        heart_rate_df : pd.DataFrame
            心拍数データ
        """
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
    
    def show_time_analysis_charts(self, intraday_hr_df, sleep_stages_df, start_time_str, end_time_str):
        """時間帯分析のグラフを表示
        
        Parameters:
        -----------
        intraday_hr_df : pd.DataFrame
            時間帯別心拍数データ
        sleep_stages_df : pd.DataFrame
            時間帯別睡眠ステージデータ
        start_time_str : str
            開始時刻文字列
        end_time_str : str
            終了時刻文字列
        """
        # ===== 心拍数データの表示 =====
        st.subheader("心拍数詳細")
        if not intraday_hr_df.empty:
            # 心拍数の時系列グラフ
            fig_intraday_hr = px.line(
                intraday_hr_df,
                x='time',
                y='heart_rate',
                title=f'心拍数の詳細変化 ({start_time_str}〜{end_time_str})',
                labels={'time': '時間', 'heart_rate': '心拍数 (bpm)'},
                markers=True
            )
            
            fig_intraday_hr.update_layout(
                xaxis_title='時間',
                yaxis_title='心拍数 (bpm)',
                yaxis={'rangemode': 'tozero'},
                hovermode='x unified'
            )
            
            # x軸のフォーマット調整
            fig_intraday_hr.update_xaxes(
                tickformat='%H:%M:%S',
                dtick=60000  # 1分間隔
            )
            
            st.plotly_chart(fig_intraday_hr, use_container_width=True)
            
            # 統計情報
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("最大心拍数", f"{int(intraday_hr_df['heart_rate'].max())} bpm", delta=None)
            with col2:
                st.metric("最小心拍数", f"{int(intraday_hr_df['heart_rate'].min())} bpm", delta=None)
            with col3:
                avg_hr = round(intraday_hr_df['heart_rate'].mean(), 1)
                st.metric("平均心拍数", f"{avg_hr} bpm", delta=None)
            
            # データリスト（展開可能）
            with st.expander("詳細データを表示"):
                st.dataframe(
                    intraday_hr_df.assign(
                        time_str=intraday_hr_df['time'].dt.strftime('%H:%M:%S')
                    )[['time_str', 'heart_rate']].rename(
                        columns={'time_str': '時間', 'heart_rate': '心拍数 (bpm)'}
                    )
                )
        else:
            st.info("この時間帯の心拍数詳細データはありません")
        
        # ===== 睡眠ステージデータの表示 =====
        st.subheader("睡眠ステージ詳細")
        if not sleep_stages_df.empty:
            sleep_stages_df = sleep_stages_df.copy()
            
            # 睡眠ステージの翻訳
            stage_mapping = {
                'wake': 'awake',  # Fitbitで使用されている場合の対応
                'awake': '覚醒',
                'light': '浅い睡眠',
                'deep': '深い睡眠',
                'rem': 'レム睡眠'
            }
            
            # 日本語表記に変換
            sleep_stages_df['sleep_stage_jp'] = sleep_stages_df['sleep_stage'].map(
                lambda x: stage_mapping.get(x, x)
            )
            
            # 色分け
            color_map = {
                '覚醒': '#FF5252',
                '浅い睡眠': '#81D4FA',
                '深い睡眠': '#1A237E',
                'レム睡眠': '#7B1FA2'
            }
            
            # 睡眠ステージをカテゴリ型に変換して表示順を制御
            stage_order = ['覚醒', '浅い睡眠', '深い睡眠', 'レム睡眠']
            sleep_stages_df['sleep_stage_jp'] = pd.Categorical(
                sleep_stages_df['sleep_stage_jp'],
                categories=stage_order,
                ordered=True
            )
            
            # 睡眠ステージのガントチャート
            fig_sleep = px.timeline(
                sleep_stages_df,
                x_start='time',
                x_end=sleep_stages_df['time'] + pd.to_timedelta(sleep_stages_df['duration_seconds'], unit='s'),
                y='sleep_stage_jp',
                color='sleep_stage_jp',
                color_discrete_map=color_map,
                title=f'睡眠ステージの変化 ({start_time_str}〜{end_time_str})'
            )
            
            fig_sleep.update_layout(
                xaxis_title='時間',
                yaxis_title='睡眠ステージ',
                xaxis={
                    'type': 'date',
                    'tickformat': '%H:%M:%S'
                },
                legend_title_text='睡眠ステージ'
            )
            
            st.plotly_chart(fig_sleep, use_container_width=True)
            
            # 統計情報
            stages_summary = sleep_stages_df.groupby('sleep_stage_jp')['duration_seconds'].sum().reset_index()
            stages_summary['duration_minutes'] = stages_summary['duration_seconds'] / 60
            
            # 円グラフで睡眠ステージの割合を表示
            fig_pie = px.pie(
                stages_summary,
                values='duration_minutes',
                names='sleep_stage_jp',
                title='睡眠ステージの割合',
                color='sleep_stage_jp',
                color_discrete_map=color_map
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # データリスト（展開可能）
            with st.expander("詳細データを表示"):
                st.dataframe(
                    sleep_stages_df.assign(
                        time_str=sleep_stages_df['time'].dt.strftime('%H:%M:%S'),
                        duration_min=sleep_stages_df['duration_seconds'] / 60
                    )[['time_str', 'sleep_stage_jp', 'duration_min']].rename(
                        columns={'time_str': '時間', 'sleep_stage_jp': '睡眠ステージ', 'duration_min': '継続時間 (分)'}
                    )
                )
        else:
            st.info("この時間帯の睡眠ステージデータはありません")
    
    def show_time_analysis_insights(self, intraday_hr_df, sleep_stages_df):
        """時間帯分析の洞察を表示
        
        Parameters:
        -----------
        intraday_hr_df : pd.DataFrame
            時間帯別心拍数データ
        sleep_stages_df : pd.DataFrame
            時間帯別睡眠ステージデータ
        """
        st.subheader("この時間帯の特徴")
        
        # 心拍数データから特徴を抽出
        if not intraday_hr_df.empty:
            hr_max = int(intraday_hr_df['heart_rate'].max())
            hr_min = int(intraday_hr_df['heart_rate'].min())
            hr_avg = round(intraday_hr_df['heart_rate'].mean(), 1)
            hr_std = round(intraday_hr_df['heart_rate'].std(), 1)
            hr_range = hr_max - hr_min
            
            # 心拍数が安定しているかどうかの判定
            is_hr_stable = hr_std < 5
            
            # 各特徴に基づいた考察
            if hr_range > 20:
                hr_pattern = "この時間帯は心拍数の変動が大きく、活動状態が変化した可能性があります。"
            elif hr_range > 10:
                hr_pattern = "この時間帯は心拍数に中程度の変動があります。"
            else:
                hr_pattern = "この時間帯は心拍数が安定しています。"
            
            if hr_avg > 90:
                hr_level = "平均心拍数が高めです。活動中または緊張状態だった可能性があります。"
            elif hr_avg > 70:
                hr_level = "平均心拍数は通常範囲内です。"
            else:
                hr_level = "平均心拍数が低めです。リラックス状態または睡眠中だった可能性があります。"
            
            st.markdown(f"""
            - **心拍数の特徴**: {hr_pattern} {hr_level}
            - **心拍変動**: 標準偏差は {hr_std} bpm で、{'安定しています' if is_hr_stable else '変動があります'}。
            """)
        
        # 睡眠データからの特徴抽出
        if not sleep_stages_df.empty:
            sleep_stages_df = sleep_stages_df.copy()
            
            # 睡眠ステージの翻訳
            stage_mapping = {
                'wake': 'awake',  # Fitbitで使用されている場合の対応
                'awake': '覚醒',
                'light': '浅い睡眠',
                'deep': '深い睡眠',
                'rem': 'レム睡眠'
            }
            
            # 日本語表記に変換
            sleep_stages_df['sleep_stage_jp'] = sleep_stages_df['sleep_stage'].map(
                lambda x: stage_mapping.get(x, x)
            )
            
            # 主要な睡眠ステージを特定
            main_stage = sleep_stages_df.groupby('sleep_stage_jp')['duration_seconds'].sum().idxmax()
            main_stage_duration = sleep_stages_df.groupby('sleep_stage_jp')['duration_seconds'].sum().max() / 60
            
            st.markdown(f"""
            - **睡眠の特徴**: この時間帯では主に「{main_stage}」状態でした（約{round(main_stage_duration, 1)}分間）。
            """)
            
            # 睡眠ステージの遷移回数
            transitions = sleep_stages_df['sleep_stage_jp'].diff().ne(0).sum() - 1
            if transitions > 0:
                st.markdown(f"- **睡眠ステージの遷移**: この時間帯で{transitions}回の睡眠ステージの変化が観測されました。") 