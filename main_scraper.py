import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time


numData = "10"#input("Enter how many cars to collect data of: ")
URL = "https://www.salvagebid.com/salvage-cars-for-sale?per_page="+numData+"&type=car"
# Instantiate an Options object
# and add the "--headless" argument
PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, chrome_options=options)
driver.get(URL)

time.sleep(5)

soup_file=driver.page_source
soup = BeautifulSoup(soup_file)
body = soup.find('body')
spa_react_root = soup.find(id="spa-react-root")
page_content = spa_react_root.find("div", class_="page-content")
# container = page_content.find("div",class_='container')
vehicle_content = page_content.find("div",class_ = "vehicle-content")
tester = spa_react_root.find("div",class_ = "result-item")



print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
print(tester.prettify())