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
import readfile
import random
import requests
import json


def auto_like(driver, file_words):
  
    #１日にいいね！できる最大値。この数を超えたら処理終了
    max_limit_likes_counter = 500
    #自動いいね！時、エラーがこの数を超えたら処理終了
    max_limit_error_cnt = 2
    #いいね！ボタン取得用
    like_x_path = '//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/section/span/button/div/span/*[name()="svg"]'

    #読み込みファイル名
    file_l_cnt = "likes_cnt.txt"
    #file_alu = "already_likes_url.txt"

    #いいね！したいワードをファイルから取得し、そのうち5つを選ぶ
    words = readfile.readWords( file_words )
    todays_like_words = []
    while len(todays_like_words) < 5:
        random_word = words[random.randint(0, len(words)-1)]
        if random_word not in todays_like_words:
            todays_like_words.append(random_word)
            
    print("本日いいねするハッシュタグ: ", todays_like_words)

    #############本日、いいね！している数をファイルから取得
    today = datetime.date.today()
    today = str(today)
    likes_cnt,data_other_than_today = readfile.getLikesCntToday(today,file_l_cnt)

    ######################すでにいいね！したURLの読み込み
    #already_likes_url = readfile.readAlreadyLikesURL(file_alu)

    #####################ハッシュタグ毎のループ
    #ハッシュタグ検索用のURL
    tag_search_url = "https://www.instagram.com/explore/tags/{}/?hl=ja"
    off = False#処理を終了する切り替えスイッチ
    error_cnt = 0
    for word in todays_like_words:

        if off:
            break
        print("http req get hashtag page: " + tag_search_url.format(word))
        driver.get(tag_search_url.format(word))
        time.sleep(6)#6秒待つ
        driver.implicitly_wait(15)

        #リンクのhref属性の値を取得
        mediaList = driver.find_elements(By.TAG_NAME, "a")
        hrefList = []

        #1つのハッシュタグに表示された画像のhrefを配列に格納
        for media in mediaList:
            href = media.get_attribute("href")
            if "/p/" in href:
                hrefList.append(href)
                print("hrefに追加しました")
        
        print("mediaListLength: ", len(mediaList))
        print("hrefListLength", len(hrefList))

        #いいねする
        for href in hrefList[9:]:
            driver.get(href)
            time.sleep(2)
            try:
                ## いいね済みチェックを追加
                likeIcon = driver.find_elements(By.XPATH, like_x_path)
                likeState = likeIcon[0].get_attribute("aria-label")

                if likeState == 'いいね！':
                    print('  まだ「いいね」してないので「いいね」します')
                    favbtn = likeIcon[0].find_element(By.XPATH, './..')
                    favbtn.click()
                    likes_cnt += 1
                    print('いいね！ {}'.format(likes_cnt))
                    time.sleep(5)
                    #follow()
                else: # '「いいね！」を取り消す'の場合
                    print('  既に「いいね」済みです。')    
                time.sleep(2)

                if "ブロックされています" in driver.page_source:
                    print("ブロックされました。処理を終了します。")
                    off = True
                    break

                flc = open(file_l_cnt,'w', encoding="utf-8")
                flc.write(data_other_than_today + today + '\t'  + str(likes_cnt) + '\n')
                flc.close()

                #この地点を通過する時にいいね！max_limit_likes_counter(デフォルト値500)回超えてたら終了
                #BAN防止
                if likes_cnt >= max_limit_likes_counter:
                    print("いいね！の上限回数({})を超えました。処理を終了します。".format(max_limit_likes_counter))
                    off = True

            except Exception as e:
                ex, ms, tb = sys.exc_info()
                print(ex)
                print(ms)
                traceback.print_tb(tb)
                error_cnt += 1
                time.sleep(5)
                if error_cnt > max_limit_error_cnt:
                    print("エラーが{}回を超えました。処理を終了します。".format(max_limit_error_cnt))
                    off = True

            if off:
                break

    print("本日のいいね！回数 {}".format(likes_cnt))
