import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time
from time import sleep

# Parameters
SITE_URL = "https://gisweb.taipei.gov.tw/TPCamp/Default.aspx"
RUN_TIME = "12:00"
LOGIN_INFO = "login_info.json"
ACCOUNT = "account"
PASSWORD = "password"
CAMPING_DATE = "1"
NUM_OF_PARTY = "2"
AREA_OPTIONS = "camping_bot_config.json"
BEGIN_TIME = time(12, 0)
END_TIME = time(17, 58)

# Launch browser
chrome_service = Service("/vboxuser/repos/driver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get(SITE_URL)

wait = WebDriverWait(driver, 10)

def do_login_taipeipass_page():
    # Open taipei pass login page
    element = wait.until(EC.element_to_be_clickable((By.ID, "link_login")))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "登入台北通")))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='./taipeipass']")))
    element.click()

    # Extract account/password from configration file and login
    f = open(LOGIN_INFO)
    data = json.load(f)
    account = wait.until(EC.element_to_be_clickable((By.ID, ACCOUNT))) 
    account.clear()
    account.send_keys(data["taipei_pass"][0][ACCOUNT])
    password = driver.find_element(By.ID, "pass")
    password.clear()
    password.send_keys(data["taipei_pass"][0][PASSWORD])
    driver.find_element(By.LINK_TEXT, "登入").click()
    f.close()

def enter_bishan_camping_booking_page():
    # Book Bishan camping area
    element = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_BT_BishanBooking"))) 
    element.click()

def check_current_time(begin_time: time, end_time: time) -> tuple[time, bool]:
    # Check current time is between 12:00 and 12:05
    # Return current time and if it is between begin and end time
    dt_now = datetime.today().time()
    current_time = time(dt_now.hour, dt_now.minute, dt_now.second)
    return current_time, (begin_time <= dt_now and dt_now <= end_time)

def book_camping_area():
    driver.refresh()
    try:
        element = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_TB_InTime_general"))) 
        element.click()
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, CAMPING_DATE))) 
        element.click()

        num_of_people = driver.find_element(By.ID, "MainContent_TB_TNum_general")
        num_of_people.clear()
        num_of_people.send_keys(NUM_OF_PARTY)

        # Extract camping area options from configration file
        wait.until(EC.element_to_be_clickable((By.ID, "Map_camp")))

        f = open(AREA_OPTIONS)
        area_options = json.load(f)
        for a in area_options:
            area_number = a.split("_")[1]
            area = driver.find_element(By.ID, a)
            if area.get_attribute("title") == "尚有空位":
                area.click()
                if "options" in area_options[a]:
                    close_btn_xpath = f"//*[@id='Modal_{area_number}']/div/div/div[1]/button"
                    wait.until(EC.element_to_be_clickable((By.XPATH, close_btn_xpath)))
                    for option in area_options[a]["options"]:
                        camping_number = option.split("_")[1]
                        if driver.find_element(By.ID, option).get_attribute("title") == "尚有空位":
                            camping_num_btn_xpath = f"//*[@id='area_{camping_number}']/div/button"
                            driver.find_element(By.XPATH, camping_num_btn_xpath).click()
                            obj = driver.switch_to.alert
                            obj.accept()
                            break
                    driver.find_element(By.XPATH, close_btn_xpath).click()
                else: 
                    break
            if int(driver.find_element(By.XPATH, "//*[@id='div_totalCamp']").text) > 0:
                break
            
        if int(driver.find_element(By.XPATH, "//*[@id='div_totalCamp']").text) == 0:
            print("On no.. All camping areas are booked...")

        f.close()
        driver.find_element(By.XPATH,"//*[@id='ctl01']/div[3]/div[2]/div/div[6]/div/div[3]/div/div[1]/div/div/div[1]/label").click()
        
        # Submit the application
        driver.find_element(By.XPATH, "//*[@id='MainContent_BT_Send_general']").click()
        return True
    except Exception as e:
        print(e)
        return False
    # finally:
        # close driver
        # driver.quit()

def do_booking_camping():
    do_login_taipeipass_page()
    enter_bishan_camping_booking_page()
    current_time, is_durring_running_time = check_current_time(BEGIN_TIME, END_TIME)
    while not is_durring_running_time:
        if current_time >= time(11, 59, 59):
            sleep(0.001)
        elif time(11, 59, 58) <= current_time < time(11, 59, 59):
            sleep(0.5)
        else:
            sleep(1)
        
        current_time, is_durring_running_time = check_current_time(BEGIN_TIME, END_TIME)
            
    book_camping_area()

# Main funtion
do_booking_camping()