#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 必要なライブラリのインポート
from math import trunc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

# 作成した関数のインポート
from auto_like import auto_like
from repost import repost

if __name__ == '__main__':
    ## このファイルはlogin.pyを1度実行している時のみ実行してください
    ## 1. 現在使っているプロファイルへのパス （chrome://version/ を開いて「プロフィール パス」から確認）をオプションに設定。
    ## login.pyを実行したのにログインされていない場合は、Defaultを削除して行ってみてください
    ## 自分の環境に合ったものだけコメントアウトを解除してください

    # (mac)
    PROFILE_PATH = "/Users/YourComputerName/Library/Application Support/Google/Chrome/Default"
    # (windows)
    # PROFILE_PATH = r"C:\Users\YOURCOMPURENAME\AppData\Local\Google\Chrome\User Data\Default"

    # (linux)
    # PROFILE_PATH = "~/.config/google-chrome"
    
    ## バックグラウンドで実行したい場合は以下の1行のコメントアウトを解除
    # options.add_argument('--headless')

    ## chromeの実行のオプションを追加
    options = Options()
    options.add_argument("--user-data-dir=" + PROFILE_PATH)
    options.add_argument("--no-sandbox")

    ## chromeを立ち上げる
    driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
    
    ## 画面の大きさを最大化する
    driver.maximize_window()

    ## 実行したい関数のコメントアウトを解除してください
    # auto_like(driver, "words_1.txt", follow_bool=True)
    repost(driver)
    # follow(driver)

    ## chromeを閉じる
    driver.close()