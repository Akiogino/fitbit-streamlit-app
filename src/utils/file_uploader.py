#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ファイルアップロード機能を提供するモジュール
"""

import os
import tempfile
import zipfile
import io
import streamlit as st

class FileUploader:
    """ファイルアップロードを処理するクラス"""
    
    @staticmethod
    def get_data_dir(data_source):
        """データソースに基づいてデータディレクトリを取得
        
        Parameters:
        -----------
        data_source : str
            データソース（'実データ', 'ローカルフォルダ', 'ZIPファイルをアップロード'）
            
        Returns:
        --------
        str
            データディレクトリのパス
        """
        if data_source == "実データ":
            data_dir = "data"
            st.sidebar.info("Fitbitデータを表示しています。実際のFitbitデータをアップロードすることもできます。")
            return data_dir
        elif data_source == "ローカルフォルダ":
            data_dir = st.sidebar.text_input("データディレクトリ", value="data")
            return data_dir
        else:
            # ZIPファイルのアップロード
            return FileUploader.handle_zip_upload()
    
    @staticmethod
    def handle_zip_upload():
        """ZIPファイルのアップロードを処理
        
        Returns:
        --------
        str
            データディレクトリのパス（一時ディレクトリまたはデモデータ）
        """
        uploaded_file = st.sidebar.file_uploader("Fitbitデータのzipファイルをアップロード", type=["zip"])
        
        if uploaded_file is not None:
            # ユーザーが自分でZIPファイルをアップロードした場合
            temp_dir = FileUploader.extract_zip(uploaded_file)
            return temp_dir
        else:
            # ZIPファイルがアップロードされなかった場合
            st.sidebar.warning("ZIPファイルをアップロードしてください")
            # デモデータを使用するオプション
            use_demo_data = st.sidebar.checkbox("実データを使用", value=True)
            if use_demo_data:
                return "data"
            else:
                st.warning("データがアップロードされていません。ZIPファイルをアップロードするか、実データを使用してください。")
                st.stop()
    
    @staticmethod
    def extract_zip(uploaded_file):
        """アップロードされたZIPファイルを一時ディレクトリに展開
        
        Parameters:
        -----------
        uploaded_file : UploadedFile
            アップロードされたZIPファイル
            
        Returns:
        --------
        str
            展開先の一時ディレクトリパス
        """
        # 一時ディレクトリを作成
        temp_dir = tempfile.mkdtemp()
        
        try:
            # ZIPファイルを読み込み
            z = zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue()))
            # すべてのファイルを一時ディレクトリに展開
            z.extractall(temp_dir)
            return temp_dir
        except Exception as e:
            st.error(f"ZIPファイルの展開中にエラーが発生しました: {e}")
            return "data"  # エラー時はデモデータを使用 