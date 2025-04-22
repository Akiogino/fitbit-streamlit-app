#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitbitデータを可視化するStreamlitアプリ（リファクタリング済み）
"""

import streamlit as st
from datetime import datetime
import pandas as pd

# リファクタリング後のモジュールをインポート
from src.ui.app_config import AppConfig
from src.utils.file_uploader import FileUploader
from src.data.loader import FitbitDataLoader
from src.ui.visualizer import FitbitVisualizer
from src.utils.auth import AuthManager
from src.analysis.ai_insights import AIAnalyzer

def main():
    """メイン関数"""
    # アプリケーション設定
    AppConfig.setup_page()
    AppConfig.show_title()
    AppConfig.show_about()
    
    # サイドバー設定
    data_source, days_to_show = AppConfig.configure_sidebar()
    
    # データディレクトリ取得
    data_dir = FileUploader.get_data_dir(data_source)
    
    # データローダー初期化
    data_loader = FitbitDataLoader(data_dir, days_to_show)
    
    # 可視化コンポーネント初期化
    visualizer = FitbitVisualizer()
    
    # データ読み込み状態を表示
    with st.spinner('データを読み込んでいます...'):
        activity_df = data_loader.load_activity_data()
        sleep_df = data_loader.load_sleep_data()
        heart_rate_df = data_loader.load_heart_rate_data()
    
    # データの有無をチェック
    if activity_df.empty and sleep_df.empty and heart_rate_df.empty:
        AppConfig.show_no_data_message(data_dir)
    
    # データの概要表示
    visualizer.show_data_summary(activity_df, sleep_df, heart_rate_df)
    
    # タブでコンテンツを整理
    tab1, tab2, tab3, tab4 = st.tabs(["歩数", "睡眠", "心拍数", "時間帯分析"])
    
    # タブ1: 歩数データ
    with tab1:
        visualizer.show_steps_chart(activity_df)
    
    # タブ2: 睡眠データ
    with tab2:
        visualizer.show_sleep_chart(sleep_df)
    
    # タブ3: 心拍数データ
    with tab3:
        visualizer.show_heart_rate_chart(heart_rate_df)
    
    # タブ4: 時間帯分析
    with tab4:
        show_time_analysis_tab(data_loader, visualizer)
    
    # フッター表示
    AppConfig.show_footer()

def show_time_analysis_tab(data_loader, visualizer):
    """時間帯分析タブの内容を表示
    
    Parameters:
    -----------
    data_loader : FitbitDataLoader
        データローダーインスタンス
    visualizer : FitbitVisualizer
        可視化コンポーネントインスタンス
    """
    st.subheader("特定時間帯の詳細分析")
    
    # アクセス制限オプション
    access_option = st.radio(
        "分析モード選択",
        ["基本分析（無料）", "AI詳細分析（認証必要）"],
        horizontal=True
    )
    
    if access_option == "AI詳細分析（認証必要）":
        # 認証マネージャー初期化
        auth_manager = AuthManager(max_api_uses=3)
        
        # アクセス制限の設定
        with st.expander("詳細分析のアクセス認証", expanded=True):
            # 認証UIを表示
            if not auth_manager.show_auth_ui():
                # 未認証の場合はここで処理を中断
                st.warning("詳細分析を利用するには認証が必要です。上記のフォームからパスワードを入力してください。")
                st.markdown("""
                ### 基本分析について
                
                基本分析モードでは、グラフや数値データのみが表示されます。
                より詳しいAI解析を利用するには、管理者からパスワードを取得してください。
                """)
                return  # 未認証の場合は処理を中断
            
            # 利用回数の上限チェック
            if not auth_manager.show_usage_limit_ui():
                return  # 制限に達している場合は処理を中断
    
    st.markdown("特定の時間帯のデータを詳しく分析します。")
    
    # 日付選択用のデータを取得
    available_dates = data_loader.get_available_dates()
    
    if not available_dates:
        st.warning("分析可能な日付データがありません")
        return
    
    # 日付選択
    date_options = [date.strftime('%Y-%m-%d') for date in available_dates]
    selected_date = st.selectbox(
        "日付を選択",
        options=date_options,
        index=0
    )
    
    # 時間帯選択
    col1, col2 = st.columns(2)
    
    # 現在時刻の取得
    now = datetime.now()
    thirty_mins_ago = now - pd.Timedelta(minutes=30)
    
    with col1:
        start_time = st.time_input("開始時間", value=thirty_mins_ago.time())
    with col2:
        end_time = st.time_input("終了時間", value=now.time())
    
    # 時間文字列に変換
    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")
    
    if st.button("分析開始"):
        # APIアクセスを使用する場合は使用回数をカウント
        if access_option == "AI詳細分析（認証必要）":
            auth_manager.increment_usage()
        
        # 心拍数の詳細データ取得
        intraday_hr_df = data_loader.load_intraday_heart_rate_data(
            target_date=selected_date,
            start_time=start_time_str,
            end_time=end_time_str
        )
        
        # 睡眠ステージデータ取得
        sleep_stages_df = data_loader.load_sleep_stages_data(
            target_date=selected_date,
            start_time=start_time_str,
            end_time=end_time_str
        )
        
        st.markdown(f"### {selected_date} {start_time_str}〜{end_time_str}の分析結果")
        
        # 時間帯分析のグラフを表示
        visualizer.show_time_analysis_charts(
            intraday_hr_df,
            sleep_stages_df,
            start_time_str,
            end_time_str
        )
        
        # 時間帯についての考察
        visualizer.show_time_analysis_insights(intraday_hr_df, sleep_stages_df)
        
        # 総合的な考察 - AIモードのみで表示
        if not intraday_hr_df.empty or not sleep_stages_df.empty:
            if access_option == "AI詳細分析（認証必要）":
                st.subheader("総合考察（AI分析）")
                
                # AIによる分析を行うかのトグル
                use_ai_insights = st.checkbox("GPT-4.1-nanoによる詳細な分析を表示", value=True)
                
                if use_ai_insights:
                    ai_analyzer = AIAnalyzer()
                    if not ai_analyzer.api_key:
                        st.warning("OpenAI APIキーが設定されていません。詳細な分析を行うには、.envファイルにOPENAI_API_KEYを設定してください。")
                        st.markdown("""
                        ### 設定方法:
                        1. プロジェクトのルートディレクトリに `.env` ファイルを作成
                        2. 以下の内容を追加:
                        ```
                        OPENAI_API_KEY=your_api_key_here
                        ```
                        3. アプリを再起動
                        """)
                    else:
                        # 状態ごとに考察を取得するキャッシュ（毎回APIを呼ばないようにする）
                        cache_key = f"{selected_date}_{start_time_str}_{end_time_str}"
                        
                        if "ai_insights" not in st.session_state:
                            st.session_state.ai_insights = {}
                        
                        # キャッシュになければ新たに生成
                        if cache_key not in st.session_state.ai_insights:
                            with st.spinner("🤖 AIが健康データを分析中..."):
                                time_range = f"{start_time_str}～{end_time_str}"
                                insights = ai_analyzer.generate_insights(
                                    intraday_hr_df, 
                                    sleep_stages_df, 
                                    selected_date, 
                                    time_range
                                )
                                st.session_state.ai_insights[cache_key] = insights
                        
                        # 結果を表示
                        st.markdown(st.session_state.ai_insights[cache_key])
                        
                        # 残り利用回数
                        remaining_uses = auth_manager.get_remaining_uses()
                        st.info(f"📊 残りAI分析回数: {remaining_uses}回")
                        
                        # 分析の注意点
                        with st.expander("💡 分析についての注意点"):
                            st.markdown("""
                            * このAI分析はGPT-4.1-nanoによって生成されています
                            * 分析結果は参考情報であり、医療アドバイスではありません
                            * より正確な健康アドバイスには、医療専門家にご相談ください
                            * 表示されている時間帯は現在時刻の30分前から現在までの活動です
                            * 健康データをリアルタイムで分析するため、同じ時間帯でも時刻によって結果が変わります
                            """)
                else:
                    # AI分析を使用しない場合は簡易的な考察を表示
                    st.markdown(f"""
                    ### 現在の時間帯データの意義
                    
                    選択されている時間帯のデータは、あなたの直近の健康状態を把握するのに役立ちます。
                    デフォルトでは、現在時刻の30分前から現在までのデータを分析します。
                    
                    この時間帯のデータを定期的に確認することで、日々の活動パターンや体調の変化をリアルタイムで把握できます。
                    特に、運動後や食事後、睡眠前後などの特定のタイミングで確認すると、より意味のある洞察が得られます。
                    
                    詳細なAI分析を表示するには、上のチェックボックスをオンにしてください。
                    """)
            else:
                # 基本分析モードの場合は簡易メッセージ
                st.info("👉 AI詳細分析を利用するには、「AI詳細分析（認証必要）」モードを選択してパスワード認証を行ってください。")
                
                # 基本的な傾向の情報を提供
                hr_avg = None
                hr_range = None
                if not intraday_hr_df.empty:
                    hr_avg = round(intraday_hr_df['heart_rate'].mean(), 1)
                    hr_range = int(intraday_hr_df['heart_rate'].max() - intraday_hr_df['heart_rate'].min())
                
                st.markdown(f"""
                ### 基本分析結果のまとめ
                
                {selected_date} {start_time_str}～{end_time_str}の時間帯で、以下の基本的な傾向が見られます：
                
                - **平均心拍数**: {hr_avg if hr_avg is not None else '不明'} bpm
                - **心拍変動**: {'大きい' if hr_range is not None and hr_range > 20 else '中程度' if hr_range is not None and hr_range > 10 else '小さい' if hr_range is not None else '不明'}
                - **主な活動状態**: {'活動中/緊張' if hr_avg is not None and hr_avg > 90 else '通常活動' if hr_avg is not None and hr_avg > 70 else 'リラックス/睡眠' if hr_avg is not None else '不明'}
                
                より詳細なAI分析と専門的なアドバイスを入手するには、認証モードに切り替えてください。
                """)

if __name__ == "__main__":
    main() 