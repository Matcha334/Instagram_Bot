# 必要なライブラリのインポート
from math import trunc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import traceback
import requests
import pyperclip
import sys, urllib
import os
import subprocess

def repost(driver):
    #repostしたい投稿のリンクを取得しブラウザで開く（クリップボードまたはファイルから）
    page_url_for_repost = 'https://www.instagram.com/p/CYRJF_4hIiK/'
    print(page_url_for_repost)
    driver.get(page_url_for_repost)

    #開いたリンクから画像をdesktopのinsta_repostフォルダに保存
    src_attribute = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/img').get_attribute("srcset").split()
    print("attribute_src:", src_attribute[0])
    
    f = open('download.jpg','wb')
    f.write(requests.get(src_attribute[0]).content)
    f.close()

    #投稿のアカウント名を読み取る
    credit_path = '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a'
    credit = driver.find_element(By.XPATH, credit_path).text
    print("クレジット: ", credit)

    #投稿アイコンをクリック
    make_post_icon_Xpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button'
    make_post_icon = driver.find_element(By.XPATH, make_post_icon_Xpath)
    make_post_icon.click()
    time.sleep(3)

    #『コンピュータから選択』ボタンをクリック
    select_button = driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
    select_button.click()
    time.sleep(3)

    #コンピュータのデスクトップのinsta_repostフォルダの最新の写真を選択
    # (mac)
    os.system("/bin/sh ./upload_image.sh")

    # (windows, linux)
    # subprocess.run(['/bin/sh', './upload_image.sh'])

    time.sleep(3)
    driver.implicitly_wait(10)
    print("ファイルをアップロードしました")
    
    #『次へ』をクリック
    next_button1 = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
    next_button1.click()
    time.sleep(5)
    print("1回目の次へボタンを押しました")
    next_button2 = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
    next_button2.click()
    time.sleep(5)
    print("2回目の次へボタンを押しました")

    #キャプションを作成(元の投稿者をメンションし、ハッシュタグをつける)
    caption = "photo by @{}\n\n----------------\n#tokyo#photographer#japan#写真好きな人と繋がりたい".format(credit)
    driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label*="キャプションを入力"]').send_keys(caption)
    time.sleep(5)

    #投稿ボタンをクリック
    share_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
    share_button.click()
    time.sleep(10)
