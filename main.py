from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

username='yourUsername'
password='yourPassword'
count=0

def login(driver):
    driver.find_element(By.NAME,"username").send_keys(username)
    driver.find_element(By.NAME,"password").send_keys(password)
    driver.find_element(By.NAME,"password").send_keys(u'\ue007')
    time.sleep(10)

def click_button_with_css(driver,css_selector):
    element=WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,css_selector))
    )
    element.click()

def navigate_to_followers(driver):
    profile_css="[href*=\""+username+"\"]"
    click_button_with_css(driver,profile_css)

def get_usernames_from_dialog(driver):
    list_className='._aano'

    try:
        followers_popup=WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,list_className))
        )
    except TimeoutException as e:
        print("The error is: ", e)
    time.sleep(5)

    users=[]
    scroll_script="arguments[0].scrollTop=arguments[0].scrollHeight;"
    while True:
        last_count = driver.find_elements(By.CLASS_NAME,"x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")
        print("last count: ", len(last_count))
        driver.execute_script(scroll_script,followers_popup)
        time.sleep(4)
        new_count = driver.find_elements(By.CLASS_NAME,"x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")

        if len(new_count) == len(last_count):
            break

    for profile in last_count:
            users.append(profile.text)

    return users

def no_followback(followers,following):
    followers.sort()
    following.sort()
    no_followback_list=[]
    for i in range(len(following)):
        try:
            followers.index(following[i])
        except ValueError:
            no_followback_list+=[following[i]]
    return no_followback_list

def __main__():
    driver = webdriver.Chrome()
   
    driver.get("https://www.instagram.com/accounts/login")

    time.sleep(5)

    login(driver)

    navigate_to_followers(driver)

    followers_css = "[href*=\""+username+"/followers/\"]"
    css_select_close = '[aria-label="Close"]'
    following_css = "[href*=\""+username+"/following/\"]"

    click_button_with_css(driver,following_css)
    following_list = get_usernames_from_dialog(driver)

    click_button_with_css(driver,css_select_close)
    print("close")
    time.sleep(5)
   
    click_button_with_css(driver,followers_css)
    followers_list = get_usernames_from_dialog(driver)

    no_followbacks = no_followback(followers_list,following_list)
    print("those people do not follow you back")
    for i in range(len(no_followbacks)):
        print(no_followbacks[i])

    return

__main__()