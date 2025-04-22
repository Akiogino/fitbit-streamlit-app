#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitbit Data Analyzer のメインエントリーポイント
コマンドラインからの実行を容易にするためのスクリプト
"""

import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Fitbit Data Analyzer - FitbitのAPIを使ってデータを取得・分析するツール"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")
    
    # トークン取得コマンド
    token_parser = subparsers.add_parser("token", help="Fitbit APIのトークンを取得")
    token_parser.add_argument("--exchange", action="store_true", help="新規トークンを取得する")
    token_parser.add_argument("--refresh", action="store_true", help="既存トークンを更新する")
    
    # データ取得コマンド
    data_parser = subparsers.add_parser("data", help="Fitbitからデータを取得")
    data_parser.add_argument("--date", default="today", help="取得する日付（例: 2023-01-01、デフォルト: today）")
    data_parser.add_argument("--days", type=int, default=1, help="取得する日数（過去に遡る日数、デフォルト: 1）")
    data_parser.add_argument("--output-dir", default="data", help="データの保存先ディレクトリ（デフォルト: data）")
    
    # 処理コマンド
    process_parser = subparsers.add_parser("process", help="取得したデータを処理")
    process_parser.add_argument("--input-dir", default="data", help="処理するデータのディレクトリ（デフォルト: data）")
    process_parser.add_argument("--output-dir", default="output", help="処理結果の保存先ディレクトリ（デフォルト: output）")
    
    # 可視化コマンド
    visualize_parser = subparsers.add_parser("visualize", help="取得したデータをPlotlyで可視化")
    visualize_parser.add_argument("--input-dir", default="data", help="可視化するデータのディレクトリ（デフォルト: data）")
    visualize_parser.add_argument("--output-dir", default="output/visualization", help="可視化結果の保存先ディレクトリ（デフォルト: output/visualization）")
    
    args = parser.parse_args()
    
    # コマンドが指定されていない場合、ヘルプを表示
    if not args.command:
        parser.print_help()
        return
    
    # スクリプトの実行パスを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 対応するコマンドを実行
    if args.command == "token":
        if args.exchange:
            from src.api.fitbit_token_exchange import main as token_exchange_main
            token_exchange_main()
        elif args.refresh:
            from src.api.fitbit_token_refresh import main as token_refresh_main
            token_refresh_main()
        else:
            token_parser.print_help()
    
    elif args.command == "data":
        # 環境変数PYTHONPATHにカレントディレクトリを追加
        sys.path.insert(0, script_dir)
        from src.api.fitbit_data_api import main as data_api_main
        
        # 元のコマンドライン引数を保存
        original_argv = sys.argv
        
        # 新しいコマンドライン引数を設定（fitbit_data_api.pyの形式に合わせる）
        sys.argv = [
            "fitbit_data_api.py", 
            "--date", args.date,
            "--days", str(args.days),
            "--output-dir", args.output_dir
        ]
        
        try:
            data_api_main()
        finally:
            # コマンドライン引数を元に戻す
            sys.argv = original_argv
    
    elif args.command == "process":
        # 環境変数PYTHONPATHにカレントディレクトリを追加
        sys.path.insert(0, script_dir)
        from src.data.fitbit_direct_process import main as direct_process_main
        
        # 元のコマンドライン引数を保存
        original_argv = sys.argv
        
        # 新しいコマンドライン引数を設定
        sys.argv = [
            "fitbit_direct_process.py",
            "--input-dir", args.input_dir,
            "--output-dir", args.output_dir
        ]
        
        try:
            direct_process_main()
        finally:
            # コマンドライン引数を元に戻す
            sys.argv = original_argv
    
    elif args.command == "visualize":
        # 環境変数PYTHONPATHにカレントディレクトリを追加
        sys.path.insert(0, script_dir)
        from src.utils.data_visualizer import main as visualizer_main
        
        # 元のコマンドライン引数を保存
        original_argv = sys.argv
        
        # 新しいコマンドライン引数を設定
        sys.argv = [
            "data_visualizer.py",
            "--input-dir", args.input_dir,
            "--output-dir", args.output_dir
        ]
        
        try:
            visualizer_main()
        finally:
            # コマンドライン引数を元に戻す
            sys.argv = original_argv

if __name__ == "__main__":
    main() 