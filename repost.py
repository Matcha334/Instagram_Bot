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
import sys, urllib
import os
import pywinauto


def repost(driver):
  #[done]repostしたい投稿のリンクを取得しブラウザで開く（クリップボードまたはファイルから）
  page_url_for_repost = "https://www.instagram.com/p/CX0ah7ZhFQ1/"
  print(page_url_for_repost)
  driver.get(page_url_for_repost)

  #[done]開いたリンクから画像をdesktopのinsta_repostフォルダに保存
  src_attribute = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/img').get_attribute("srcset").split()
  print("attribute_src:", src_attribute[0])
  
  f = open('download.jpg','wb')
  f.write(requests.get(src_attribute[0]).content)
  f.close()

  #[done]投稿のアカウント名を読み取る
  credit_path = '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a'
  credit = driver.find_element(By.XPATH, credit_path).text
  print("クレジット: ", credit)

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
  #mac
  # os.system("/bin/sh ./upload_image.sh")
  # 開くダイアログを探して接続する
  findWindow = lambda: pywinauto.findwindows.find_windows(title=u'開く')[0]
  dialog = pywinauto.timings.wait_until_passes(5, 1, findWindow)

  pwa_app = pywinauto.Application()
  pwa_app.connect(handle=dialog)

  window = pwa_app[u"開く"]

  # テキストボックス(ファイル名)にPATHを入力
  tb = window[u"ファイル名(&N):"]
  if tb.is_enabled():
      tb.click()
      edit = window.Edit4
      edit.set_focus()
      edit.set_text(r"C:\Users\yamag\OneDrive\デスクトップ\MyProgramming\instagram_bot\origianl_instagram_bot\download.jpg")

  # 開くボタンを押す（Alt+O）
  pywinauto.keyboard.send_keys("%O")
        
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
  caption = "photo by @{}\n\n-----------\n#tokyo#photographer#japan#写真好きな人と繋がりたい".format(credit)
  caption_path = '/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea'
  captionField = driver.find_element(By.XPATH, caption_path)
  captionField.send_keys(caption)
  time.sleep(5)

  #投稿ボタンをクリック
  share_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
  share_button.click()
  time.sleep(10)
