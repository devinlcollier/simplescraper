from time import sleep
from selenium import webdriver
import sys

driver = webdriver.Firefox()
driver.get("https://duckduckgo.com/")

sleep(3)

driver.maximize_window()

sleep(5)
driver.close()