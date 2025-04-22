#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI APIを使用してFitbitデータに基づく洞察を生成するモジュール
"""

import os
import json
import streamlit as st
import openai
import time
import requests
from dotenv import load_dotenv

class AIAnalyzer:
    """AIを使用してデータを分析するクラス"""
    
    def __init__(self):
        """初期化"""
        # 環境変数の読み込み
        load_dotenv()
        
        # OpenAI APIキーの設定
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_insights(self, heart_rate_data, sleep_data, target_date, time_range):
        """OpenAI GPT-4.1 nanoを使用して健康データに基づく洞察を生成する
        
        Parameters:
        -----------
        heart_rate_data : pd.DataFrame
            時間帯ごとの心拍数データ
        sleep_data : pd.DataFrame
            時間帯ごとの睡眠ステージデータ
        target_date : str
            対象日
        time_range : str
            対象時間帯
        
        Returns:
        --------
        str
            生成された洞察テキスト
        """
        if not self.api_key:
            return "**注意**: OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。"
        
        try:
            # 分析のためのデータ要約を作成
            hr_stats = {}
            sleep_stats = {}
            
            if not heart_rate_data.empty:
                hr_stats = {
                    "平均心拍数": round(heart_rate_data['heart_rate'].mean(), 1),
                    "最大心拍数": int(heart_rate_data['heart_rate'].max()),
                    "最小心拍数": int(heart_rate_data['heart_rate'].min()),
                    "心拍数標準偏差": round(heart_rate_data['heart_rate'].std(), 1),
                    "心拍数変動範囲": int(heart_rate_data['heart_rate'].max() - heart_rate_data['heart_rate'].min())
                }
            
            if not sleep_data.empty:
                # 睡眠ステージ分布
                stage_distribution = sleep_data.groupby('sleep_stage')['duration_seconds'].sum()
                stage_distribution = (stage_distribution / 60).to_dict()  # 分単位に変換
                
                # 主な睡眠ステージ
                if not stage_distribution:
                    main_stage = "不明"
                else:
                    main_stage = max(stage_distribution.items(), key=lambda x: x[1])[0]
                
                # 睡眠ステージの遷移回数
                transitions = sleep_data['sleep_stage'].diff().ne(0).sum() - 1 if len(sleep_data) > 1 else 0
                
                sleep_stats = {
                    "主な睡眠ステージ": main_stage,
                    "睡眠ステージ分布（分）": stage_distribution,
                    "睡眠ステージ遷移回数": transitions
                }
            
            # OpenAI APIリクエスト用のデータ
            prompt = f"""
            あなたは健康データ分析のエキスパートです。Fitbitから取得した特定時間帯（{time_range}）の{target_date}のデータに基づいて、健康状態や生活習慣について洞察を提供してください。

            データの概要：
            
            心拍数データ:
            {json.dumps(hr_stats, ensure_ascii=False, indent=2) if hr_stats else "データなし"}
            
            睡眠ステージデータ:
            {json.dumps(sleep_stats, ensure_ascii=False, indent=2) if sleep_stats else "データなし"}
            
            以下の点について考察してください：
            1. この時間帯のデータが示す健康状態について
            2. 生活習慣や睡眠の質への影響
            3. 健康改善のための具体的な提案（該当する場合）
            4. 特に注目すべきパターンや特徴
            
            回答は日本語で、科学的根拠に基づいた専門的で分かりやすい内容にしてください。箇条書きも適宜使い、読みやすく構成してください。
            医学的見地からの総合的な考察をお願いします。
            """
            
            return self._call_openai_api(prompt)
            
        except Exception as e:
            st.error(f"AIによる洞察生成中にエラーが発生しました: {str(e)}")
            return f"**エラー**: AI洞察を生成できませんでした。詳細: {str(e)}"
    
    def _call_openai_api(self, prompt):
        """OpenAI APIを呼び出す
        
        Parameters:
        -----------
        prompt : str
            APIに送るプロンプト
            
        Returns:
        --------
        str
            APIからの応答テキスト
        """
        try:
            # OpenAI APIの呼び出し
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4.1-nano",  # GPT-4.1 Nano
                messages=[
                    {"role": "system", "content": "あなたは健康データ分析の専門家です。科学的根拠に基づいた洞察を提供します。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # 結果を返す
            insight_text = response.choices[0].message.content
            return insight_text
            
        except Exception as e:
            # API呼び出しに失敗した場合は標準的なAPIを使う
            st.error(f"GPT-4.1-nanoでの分析中にエラーが発生しました: {str(e)}")
            st.warning("標準的なOpenAI APIを使用して再試行します...")
            
            try:
                # 標準的なAPIリクエスト
                import requests
                
                api_key = self.api_key
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                
                payload = {
                    "model": "gpt-4.1-nano",
                    "messages": [
                        {"role": "system", "content": "あなたは健康データ分析の専門家です。科学的根拠に基づいた洞察を提供します。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                
                return result["choices"][0]["message"]["content"]
                
            except Exception as sub_e:
                return f"""
                **エラー**: GPT-4.1-nanoを使用したAI洞察生成に失敗しました。

                詳細エラー情報:
                1. {str(e)}
                2. {str(sub_e)}
                
                解決方法:
                - OpenAI APIキーが正しく設定されているか確認してください
                - OpenAIアカウントでGPT-4.1-nanoにアクセス権があるか確認してください
                - APIの利用制限に達していないか確認してください
                """ 