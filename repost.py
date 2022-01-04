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
import pyperclip
import sys, urllib
import os.path

#例えばJupyterLabやブラウザを立ち上げた状態でスクリーンショットを撮って保存する
import pyautogui
sc = pyautogui.screenshot("fullscreen.png")

def repost(driver):
  #[done]repostしたい投稿のリンクを取得しブラウザで開く（クリップボードまたはファイルから）
  page_url_for_repost = pyperclip.paste()
  driver.get(page_url_for_repost)

  #開いたリンクから画像をdesktopのinsta_repostフォルダに保存
  ##################################
  #https://dixq.net/forum/viewtopic.php?t=16930
  img = urllib.urlopen(page_url_for_repost)
  localfile = open( os.path.basename(page_url_for_repost), 'wb')
  localfile.write(img.read())
  img.close()
  localfile.close()
  ###############################

  #[done]投稿のアカウント名を読み取る
  credit = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a')

  #[done]投稿アイコンをクリック
  make_post_icon_Xpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button'
  make_post_icon = driver.find_element(By.XPATH, make_post_icon_Xpath)
  make_post_icon.click()
  time.sleep(3)
  #[done]『コンピュータから選択』ボタンをクリック
  select_button = driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
  select_button.click()
  time.sleep(3)

  #コンピュータのデスクトップのinsta_repostフォルダの最新の写真を選択

  #『次へ』をクリック

  #[done]キャプションを作成(元の投稿者をメンションし、ハッシュタグをつける)
  caption = "📸 @{}\n\n-----------\n#tokyo#photographer#japan#写真好きな人と繋がりたい".format(credit)

  #投稿ボタンをクリック
