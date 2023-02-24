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

# Launch browser
chrome_service = Service("/vboxuser/repos/driver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--user-data-dir=/home/vboxuser/.config/google-chrome")
# chrome_options.add_argument("--profile-directory=Profile 3")

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
wait.until(EC.element_to_be_clickable((By.ID, "MainContent_BT_BishanBooking"))) 
driver.find_element(By.ID, "MainContent_BT_BishanBooking").click()

wait.until(EC.element_to_be_clickable((By.ID, "MainContent_TB_InTime_general"))) 
# campTime = driver.find_element(By.ID, "MainContent_TB_InTime_general")
# campTime.clear()
# campTime.send_keys("2023/03/03")

numOfPpl = driver.find_element(By.ID, "MainContent_TB_TNum_general")
numOfPpl.clear()
numOfPpl.send_keys("2")



# close browser
# driver.quit()


# extract config file and input data
# sleap vs webdriver wait
# How to insert date