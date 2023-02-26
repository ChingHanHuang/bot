import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Parameters
SITE_URL = "https://gisweb.taipei.gov.tw/TPCamp/Default.aspx"
LOGIN_INFO = "login_info.json"
ACCOUNT = "account"
PASSWORD = "password"
CAMPING_DATE = "16"
NUM_OF_PPL = "2"
AREA_OPTIONS = "camping_bot_config.json"

# Launch browser
chrome_service = Service("/vboxuser/repos/driver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get(SITE_URL)

# Open taipei pass login page
wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable((By.ID, "link_login")))
driver.find_element(By.ID, "link_login").click()

wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "登入台北通")))
driver.find_element(By.LINK_TEXT, "登入台北通").click()

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='./taipeipass']")))
driver.find_element(By.XPATH, "//a[@href='./taipeipass']").click()

# Extract account/password from configration file and login
f = open(LOGIN_INFO)
data = json.load(f)

wait.until(EC.element_to_be_clickable((By.ID, ACCOUNT))) 
account = driver.find_element(By.ID, ACCOUNT)
account.clear()
account.send_keys(data["taipei_pass"][0][ACCOUNT])
password = driver.find_element(By.ID, "pass")
password.clear()
password.send_keys(data["taipei_pass"][0][PASSWORD])
driver.find_element(By.LINK_TEXT, "登入").click()

f.close()

# Book Bishan camping area
time.sleep(0.5)
wait.until(EC.element_to_be_clickable((By.ID, "MainContent_BT_BishanBooking"))) 
driver.find_element(By.ID, "MainContent_BT_BishanBooking").click()

wait.until(EC.element_to_be_clickable((By.ID, "MainContent_TB_InTime_general"))) 
driver.find_element(By.ID, "MainContent_TB_InTime_general").click()
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, CAMPING_DATE))) 
driver.find_element(By.LINK_TEXT, CAMPING_DATE).click()

num_of_people = driver.find_element(By.ID, "MainContent_TB_TNum_general")
num_of_people.clear()
num_of_people.send_keys(NUM_OF_PPL)

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
f.close()

driver.find_element(By.XPATH,"//*[@id='ctl01']/div[3]/div[2]/div/div[6]/div/div[3]/div/div[1]/div/div/div[1]/label").click()

# Submit the application
# driver.find_element(By.XPATH, "//*[@id='MainContent_BT_Send_general']").click()

# close browser
# driver.quit()


# how to handle TimeoutError 
# wait till 12 PM to start to book
# sleep vs webdriver wait