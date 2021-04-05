from selenium import webdriver
import chromedriver_binary
import time

driver = webdriver.Chrome()

driver.get('https://www.google.co.jp/')

time.sleep(5)

driver.quit()
