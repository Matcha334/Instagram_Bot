# 必要なライブラリのインポート
from math import trunc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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