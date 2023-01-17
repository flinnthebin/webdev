##!/usr/bin/python3

import time
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.bunnings.com.au/90-x-45mm-outdoor-framing-mgp10-h3-treated-pine-5-4m_p8032182"

# create a browser instance
browser = webdriver.Firefox()

# load the website
browser.get(url)

# wait for the JavaScript to execute
time.sleep(5)

# extract the html source
html = browser.page_source

# close the browser
browser.quit()

soup = BeautifulSoup(html, 'lxml')

price = soup.find("p", class_="sc-cb9c4042-3 iGDFOw").text

print(price)
