#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import random
import requests
import json

from auto_like import auto_like
from login import login
from repost import repost

# def get_profile_info():
    # API_Key = ""
    # headers = {'Content-Type': 'application/json', 'key':API_Key}
    # data = {'client_id':'xxxxxxxxxxxxxxxxxx',
    # 'client_secret':'xxxxxxxxxxxxxxxxxx',
    # 'grant_type':'authorization_code', 
    # 'redirect_uri':'http://localhost:14080/newpage', 
    # 'code':code}        

    # token_url = 'https://api.instagram.com/oauth/access_token'
    # result = requests.get(token_url, params = data)
    # print("api result:", result)

if __name__ == '__main__':

    #Chromeを起動
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("--no-sandbox")

    #現在使っているプロファイルへのパス （chrome://version/ を開いて「プロフィール パス」から確認）
    # 1. 自分のpcで行う場合
    PROFILE_PATH = "/Users/[YourComputerName]/Library/Application Support/Google/Chrome/Default"
    # 2. aws ec2上にインストールしたchromeで行う場合
    # PROFILE_PATH = "~/.config/google-chrome"
    options.add_argument("--user-data-dir=" + PROFILE_PATH)

    driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
    driver.maximize_window()
    # 関数実行
    # login(driver,username="kanacoriander", password="style1234")
    # auto_like(driver, file_words="words_1.txt")
    repost(driver)
    #ブラウザを閉じる
    driver.close()