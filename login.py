# 必要なライブラリのインポート
from math import trunc
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse
import time
import datetime
import sys
import traceback
import auto_like
import random
import requests
import json

def login(driver, username, password):
    #Instagram ログインURL
    login_url = "https://www.instagram.com/"

    #ログイン用フォームへのパス
    username_path = '//form//div[1]//input'
    password_path = '//form//div[2]//input'

    #Instagramのサイトを開く
    driver.get(login_url)
    time.sleep(3)

    #ユーザー名とパスワードを入力してリターンキーを押す
    usernameField = driver.find_element(By.XPATH, username_path)
    usernameField.send_keys(username)
    time.sleep(1)
    passwordField = driver.find_element(By.XPATH, password_path)
    passwordField.send_keys(password)
    passwordField.send_keys(Keys.RETURN)
    time.sleep(3)

    if "アカウントが不正使用されました" in driver.page_source:
        print(driver.page_source)
        print("ブロックされました。パスワードを変更する必要があります。")
        print("処理を終了します。")
        exit()

if __name__ == '__main__':
    # 自分の環境に合ったものだけコメントアウトを解除してください
    # login.pyを実行したのにログインされていない場合は、Defaultを削除して行ってみてください

    # (mac)
    PROFILE_PATH = "/Users/YourComputerName/Library/Application Support/Google/Chrome/Default"
    # (windows)
    # PROFILE_PATH = "C:\Users\Alice\AppData\Local\Google\Chrome\User Data\Default"

    # (linux)
    # PROFILE_PATH = "~/.config/google-chrome"
    
    # 2. バックグラウンドで実行したい場合は以下の1行のコメントアウトを解除
    # options.add_argument('--headless')

    # chromeの実行のオプションを追加
    options = Options()
    options.add_argument("--user-data-dir=" + PROFILE_PATH)
    options.add_argument("--no-sandbox")

    #chromeを立ち上げる
    driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
    
    #画面の大きさを最大化する
    driver.maximize_window()

    # 関数実行
    login(driver, "YourUsername", "YourPassword")
    driver.close()