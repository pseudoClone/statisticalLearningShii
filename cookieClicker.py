from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service()
driver = webdriver.Firefox(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

cookieID = "bigCookie"

# Selecting the languge
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='langSelect-EN']"))
)

language = driver.find_element(By.XPATH, "//*[@id='langSelect-EN']")
language.click()

# Wait for cookie to appear
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, cookieID))
)

cookie = driver.find_element(By.ID, cookieID)
cookie.click()
time.sleep(10) # In seconds
