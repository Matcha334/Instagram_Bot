from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")

#現在使っているプロファイルへのパス （chrome://version/ を開いて「プロフィール パス」から確認）
# 1. 自分のpcで行う場合
# PROFILE_PATH = "/Users/hamadakanako/Library/Application Support/Google/Chrome/Default"
# 2. aws ec2上にインストールしたchromeで行う場合
PROFILE_PATH = "~/.config/google-chrome"

options.add_argument("--user-data-dir=" + PROFILE_PATH)

driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
driver.maximize_window()
driver.get('https://www.instagram.com/')

print("アクセス完了")
sleep(5)

driver.close()