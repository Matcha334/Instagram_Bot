from selenium.webdriver.common.by import By
import time

def follow(driver):
    #profile_path = '//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/div/header/div/div/div/span/a'
    # profile_button = driver.find_elements(By.XPATH, profile_path)

    follow_button_path = '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button'
    follow_state = driver.find_element(By.XPATH, follow_button_path).text
    print("follow_state: ", follow_state)
    credit = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a').text
    if follow_state == "フォローする":
        profile_link = "https://www.instagram.com/" + credit
        driver.get(profile_link)
        time.sleep(3)

        follower = driver.find_elements(By.CLASS_NAME,'g47SY')[1].get_attribute("title")
        
        follower= int (follower.replace(',',''))
        if follower == 0:
            follower = follower + 1

        follow = driver.find_elements(By.CLASS_NAME,'g47SY')[2].text
        follow= int (follow.replace(',',''))
        follow_count=0
        follow_max=3
        print("follower num : ", follower, "follow num: ", follow)
        if(follow_count>follow_max):
            print("一日のフォロー上限に達しました")
            off=True
        #毎日すべて止まる可能性がある、できればこのフォローのみを終わらせて他は引き続き実行し続けておきたい
       # elif (int(follow)/int(follower)) >= 1:
        else:
           profile_follow_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button')
           profile_follow_button.click()
           print("フォローしました")
           time.sleep(3)
           follow_count+=1
            

            
        

        