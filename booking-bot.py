import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# parameters
site_url = 'https://www.morningbrew.com/daily'
chrome_service = Service('/vboxuser/repos/driver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://www.theodinproject.com/lessons/foundations-html-boilerplate")

time.sleep(3)
print('Title: %s' % driver.title)
#driver.quit()