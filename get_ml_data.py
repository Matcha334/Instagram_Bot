from os import error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
import urllib.request as req
import pandas as pd
import re
import bs4
import time
from login import login
 
INSTAGRAM_DOMAIN = "https://www.instagram.com"
MIN_COUNT = 100
KEYWORD = "都庁"
CHROMEDRIVER = "/Users/bishop/Desktop/origianl_instagram_bot/chromedriver"
PROFILE_PATH = "/Users/bishop/Library/Application Support/Google/Chrome/Default"

# driver取得
def get_driver():
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    # options.add_argument('--headless')
    # ブラウザーを起動
    options.add_argument("--user-data-dir=" + PROFILE_PATH)
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
      
    return driver
 
# 対象ページ取得
def get_text_from_target_page(driver, first_flg, url):
    
    # ターゲット
    driver.get(url)
    try:
        # articleタグが読み込まれるまで待機（最大10秒）
        # headerタグが読み込まれるまで待機（最大10秒）
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'header')))
    except Exception as error:
        print(f"error: {error}")
        driver.implicitly_wait(30)  # 見つからないときは、15秒まで待つ
        driver.refresh()
        print("refreshed")
      
    text = driver.page_source
    return text
 
# 正規表現で値を抽出
def get_search_value(ptn, str):
      
    result = re.search(ptn, str)
      
    if result:
        return result.group(1)
    else:
        return None
     
#検索結果の一覧からpost_urlとimg_srcを取得
def get_info_from_text(text):
    soup = bs4.BeautifulSoup(text, features='lxml')
    try:
        #空の辞書型の作成
        info = {}

        #投稿の取得
        post_elems = soup.find_all(class_="v1Nh3")
        for elem in post_elems:
            #投稿idの取得
            a_elem = elem.find("a")
            href = a_elem["href"]    
            post_url = INSTAGRAM_DOMAIN + href
            post_id = get_search_value("\/p\/(.*)\/", href)
            
            #画像リンクの取得
            img_elem = elem.find("img")
            img_src = img_elem["src"]
             
            #infoに代入
            tmp_dict = {}
            tmp_dict['post_url'] = post_url
            tmp_dict['img_src'] = img_src
                     
            info[post_id] = tmp_dict     
        return info
         
    except Exception as error:
        print(f"error: {error}")
        return None
     
def get_detail_form_info(driver, text):
    soup = bs4.BeautifulSoup(text, features='lxml')
    try:
        #空の辞書型を作成
        detail = {}

        #いいねの数を取得
        like_elems = soup.find_all(class_="Nm9Fw")[0]
        likes = like_elems.find('span').contents[0]
        detail['likes'] = likes

        #フォロワー、フォロー数の取得
        user_elems = soup.find_all(class_="e1e1d")[0]
        username = user_elems.find('a')['href']
        profile_url = "https://www.instagram.com" + username
        text_2 = get_text_from_target_page(driver, 'header', profile_url)
        time.sleep(2)
        profile_html = bs4.BeautifulSoup(text_2, features='lxml')
        follower_elems = profile_html.find_all(class_="Y8-fY")[1]
        detail['followers'] = follower_elems.find('a').find('span').contents[0]
        following_elems = profile_html.find_all(class_="Y8-fY")[2]
        detail['following'] = following_elems.find('a').find('span').contents[0]

        #投稿日時の取得
        date_elems = soup.find_all(class_="PIoXz")[0]
        detail['date'] = [obj['datetime'] for obj in date_elems.find_all('time') if obj.has_attr('datetime')][0]

        #概要の取得
        caption_elems = soup.find_all(class_="C4VMK")[0]
        detail['caption'] = caption_elems.find_all('span')[1].get_text()
        return detail
    
    except Exception as error:
        print(f"error: {error}")
        return None
    

# 最後の要素までスクロール
def scroll_to_elem(driver, footer_move_flg):
     
    try:
        if footer_move_flg:
            #最後まで移動
            last_elem = driver.find_element_by_id("fb-root")   
            actions = ActionChains(driver)
            actions.move_to_element(last_elem)
            actions.perform()
        else: 
            #最後の要素の一つ前までスクロール
            row_elems = driver.find_elements_by_class_name("weEfm")
            #検索結果一覧を1行ずつ取得
            # row_elems = driver.find_all(_class="weEfm")
            last_elem = row_elems[-1]
            actions = ActionChains(driver)
            actions.move_to_element(last_elem)
            actions.perform()
        return True
    except:
        return False
 
# 投稿件数取得
def get_post_count(text):
    try:
        # json_str = get_search_value("window._sharedData = (.*)<\/script>", text)
        # dict = json.loads(json_str)
        # print(f"dict: {dict}")
        # post_count = dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
        soup = bs4.BeautifulSoup(text, features='lxml')
        header_elems = soup.find_all('WSpok')[0]
        all_post_count = header_elems.find_all('span')[1].contents[0]
        return all_post_count
    except Exception as error:
        print(f"error: {error}")
        return MIN_COUNT
     
if __name__ == '__main__':
    start = time.time()

    #検索結果ページのurl
    url = "https://www.instagram.com/explore/tags/" + urllib.parse.quote(KEYWORD) + "/"
 
    # ブラウザーを起動
    driver = get_driver()
    # login(driver,username="okumataro03", password="qwertywinc")

    #検索結果ページのhtmlソース取得
    text_0 = get_text_from_target_page(driver, True, url)
    all_post_count = get_post_count(text_0)
    print("合計検索結果：" + str(all_post_count)) #投稿件数の出力
     
    info_all = {} 
    count_info = 0 #読み込み済み検索結果件数
    buf_count_info = 0 #一画面に表示できる
    while count_info < MIN_COUNT:
        # スクロール後対象ページのhtmlソース取得
        text_1 = driver.page_source
        info = get_info_from_text(text_1)
        # print(f"url: {info.get('post_url')}")
         
        if info != None:
            info_all.update(info)
         
        count_info = len(info_all) 
        time.sleep(1)
        print(f"count_info: {count_info}")
        print(f"buf_count_info: {buf_count_info}")
         
        if buf_count_info==count_info: #表示可能件数が全投稿数と一致するなら待つ??
            time.sleep(3)
             
        result_flg = scroll_to_elem(driver, False)
        buf_count_info = count_info 
         
        if all_post_count <= count_info: #全投稿数が取得件数より少ない
            break

    print("データを出力中...")
    for info in info_all:
        info = info_all.get(info)
        url = info.get('post_url')

        text_1 = get_text_from_target_page(driver, 'article', url)
        time.sleep(2)
        detail = get_detail_form_info(driver, text_1)
        if detail != None:
            info.update(detail)
    driver.quit()

    print(f"{count_info}件データを取得しました")

    df = pd.DataFrame(info_all).T
    df.to_csv(f'{KEYWORD}{count_info}.csv', encoding='utf_8_sig')

    elapsed_time = time.time() - start
    m, s = divmod(elapsed_time, 60)
    print(f"処理に{int(m)}分{int(s)}秒かかりました")
