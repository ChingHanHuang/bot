import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# parameters
site_url = 'https://www.morningbrew.com/daily'
 
driver = webdriver.Chrome(service=Service('/vboxuser/repos/driver'))

driver.get("https://www.theodinproject.com/lessons/foundations-html-boilerplate")
time.sleep(3)
print('Title: %s' % driver.title)
#driver.quit()