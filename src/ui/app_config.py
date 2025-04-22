#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
アプリケーション設定を提供するモジュール
"""

import streamlit as st

class AppConfig:
    """アプリケーション設定クラス"""
    
    @staticmethod
    def setup_page():
        """ページの基本設定を行う"""
        st.set_page_config(
            page_title="Fitbit データ分析ダッシュボード - 健康追跡の可視化",
            page_icon="💓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def show_title():
        """アプリのタイトルとヘッダーを表示"""
        st.title("Fitbit データ分析ダッシュボード")
        st.markdown("### 健康データの可視化・研究分析ツール")
    
    @staticmethod
    def show_about():
        """アプリの説明を表示"""
        with st.expander("このアプリについて"):
            st.markdown("""
            ### Fitbit データ分析ダッシュボードとは？
            
            このアプリは、Fitbitから取得したデータを視覚化・分析するための研究用ツールです。以下の機能があります：
            
            1. **歩数の推移**: 日々の歩数を確認し、目標（10,000歩）との比較ができます
            2. **睡眠時間の推移**: 睡眠時間をグラフ化し、推奨睡眠時間（7-9時間）との比較ができます
            3. **心拍数の推移**: 安静時心拍数の変化を追跡できます
            
            ### データについて
            
            このアプリで使用しているデータは、2025年3月〜4月のFitbitデバイスから取得した実際のデータに基づいています。
            データはプライバシーに配慮して処理されています。
            """)
    
    @staticmethod
    def show_footer():
        """フッターを表示"""
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center;">
            <p>このアプリはFitbitデータを可視化するための研究用ツールです。</p>
            <p>2025年3月〜4月のデータを元に作成されています。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("© 2024 健康データ研究プロジェクト")
    
    @staticmethod
    def configure_sidebar():
        """サイドバーの設定を行う"""
        st.sidebar.header("設定")
        
        # データソース選択
        data_source = st.sidebar.radio(
            "データソース",
            ["実データ", "ローカルフォルダ", "ZIPファイルをアップロード"],
            index=0
        )
        
        # 表示設定
        days_to_show = st.sidebar.slider("表示する日数", min_value=7, max_value=90, value=30)
        
        return data_source, days_to_show
    
    @staticmethod
    def show_no_data_message(data_dir):
        """データが見つからない場合のメッセージを表示"""
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