from selenium.webdriver.common.by import By
import time

def follow(driver):
    #profile_path = '//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/div/header/div/div/div/span/a'
    # profile_button = driver.find_elements(By.XPATH, profile_path)
    follow_button_path = '/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button'
    driver.implicitly_wait(10)
    follow_button = driver.find_element(By.XPATH, follow_button_path)
    follow_state = follow_button.text
    print("follow_state: ", follow_state)
    if follow_state == "フォローする":
        time.sleep(5)
        profile_link = "https://www.instagram.com/" + driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a')
        driver.get(profile_link)
        time.sleep(3)

        follower = driver.find_elements(By.CLASS_NAME,'g47SY')[1].get_attribute("title")
        if follower == 0:
            follower = follower + 1

        follow = driver.find_elements(By.CLASS_NAME,'g47SY')[2].get_attribute("title")
        print("follower num : ", follower, "follow num: ", follow)
        if (follow/follower) >= 1:
            profile_follow_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button')
            profile_follow_button.click()
            print("フォローしました")