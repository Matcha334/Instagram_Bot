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
from login import login

if __name__ == '__main__':
    ## 自分の環境を入力してください ##
    #####################################
    webdriver_path = "/usr/local/bin/chromedriver"
    your_env = "mac" # mac, windows, linux
    your_computer_name = "hamadakanako"
    logged_in = True #ログインしているか否か
    username = ""
    password = ""
    #######################################


    if your_env == "mac":
        PROFILE_PATH = "/Users/{}/Library/Application Support/Google/Chrome/Default".format(your_computer_name)
    elif your_env == "windows":
        PROFILE_PATH = "C:/Users/{}/AppData/Local/Google/Chrome/User Data/Default".format(your_computer_name)
    else:
        PROFILE_PATH = "~/.config/google-chrome"
    

    ## chromeの実行のオプションを追加
    options = Options()
    ## バックグラウンドで実行したい場合は以下の1行のコメントアウトを解除
    # options.add_argument('--headless')
    options.add_argument("--user-data-dir=" + PROFILE_PATH)
    options.add_argument("--no-sandbox")

    ## chromeを立ち上げる
    driver = webdriver.Chrome(options=options, executable_path=webdriver_path)
    
    ## 画面の大きさを最大化する
    driver.maximize_window()

    if not logged_in:
        login(driver, username, password)

    ## 実行したい関数のコメントアウトを解除してください
    auto_like(driver, follow_bool=True) #True or Falseを入力
    repost(driver)

    ## chromeを閉じる
    driver.close()