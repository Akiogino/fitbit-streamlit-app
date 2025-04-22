#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
認証機能を提供するモジュール
"""

import os
import streamlit as st
from dotenv import load_dotenv

class AuthManager:
    """認証管理クラス"""
    
    def __init__(self, max_api_uses=3):
        """
        初期化
        
        Parameters:
        -----------
        max_api_uses : int
            1セッションあたりの最大API使用回数
        """
        # 環境変数の読み込み
        load_dotenv()
        
        # 分析パスワードの設定
        self.password = os.getenv("ANALYSIS_PASSWORD", "fitbit-analysis-demo")
        self.max_api_uses = max_api_uses
        
        # セッション状態の初期化
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'api_usage_count' not in st.session_state:
            st.session_state.api_usage_count = 0
        if 'max_api_uses' not in st.session_state:
            st.session_state.max_api_uses = max_api_uses
    
    def is_authenticated(self):
        """認証済みかどうかを確認する"""
        return st.session_state.authenticated
    
    def authenticate(self, password):
        """パスワードを使用して認証する
        
        Parameters:
        -----------
        password : str
            入力されたパスワード
            
        Returns:
        --------
        bool
            認証成功の場合はTrue、それ以外はFalse
        """
        if password == self.password:
            st.session_state.authenticated = True
            return True
        return False
    
    def increment_usage(self):
        """API使用回数をインクリメントする"""
        st.session_state.api_usage_count += 1
    
    def reset_usage(self):
        """API使用回数をリセットする"""
        st.session_state.api_usage_count = 0
    
    def get_remaining_uses(self):
        """残りのAPI使用回数を取得する
        
        Returns:
        --------
        int
            残りの使用回数
        """
        return st.session_state.max_api_uses - st.session_state.api_usage_count
    
    def can_use_api(self):
        """APIを使用できるかどうかを確認する
        
        Returns:
        --------
        bool
            APIを使用できる場合はTrue、それ以外はFalse
        """
        return (
            st.session_state.authenticated and 
            st.session_state.api_usage_count < st.session_state.max_api_uses
        )
    
    def show_auth_ui(self):
        """認証UIを表示する
        
        Returns:
        --------
        bool
            認証が成功した場合はTrue、それ以外はFalse
        """
        if self.is_authenticated():
            st.success(f"✅ 認証済み - 残り利用回数: {self.get_remaining_uses()}回")
            return True
        else:
            # 認証フォーム
            password = st.text_input("アクセスパスワードを入力", type="password")
            
            if st.button("認証"):
                if self.authenticate(password):
                    st.success("✅ 認証に成功しました！詳細分析機能が利用可能になりました。")
                    st.rerun()  # 画面を更新
                    return True
                else:
                    st.error("❌ パスワードが正しくありません。管理者にお問い合わせください。")
            
            return False
    
    def show_usage_limit_ui(self):
        """使用制限UIを表示する
        
        Returns:
        --------
        bool
            制限がリセットされた場合はTrue、それ以外はFalse
        """
        if not self.can_use_api():
            st.warning(f"⚠️ APIの利用回数制限（{self.max_api_uses}回）に達しました。管理者にお問い合わせください。")
            if st.button("利用制限をリセット（デモ用）"):
                self.reset_usage()
                st.success("利用回数をリセットしました！")
                st.rerun()
                return True
            return False
        return True 