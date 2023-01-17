##!/usr/bin/python3

import time
from bs4 import BeautifulSoup
from selenium import webdriver

class Scraper:

  def retrieve_html(self, url: str) -> str:
    # open browser, retrieve html
    browser = webdriver.Firefox()
    browser.get(url)
    # allow javascript to render elements
    time.sleep(5)
    # create html variable, close browser
    html = browser.page_source
    browser.quit()
    return html
  
  def soup_finder(self, html: str, tag: str, classname: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    price = soup.find(tag, class_=classname).text
    return price

url = "https://www.bunnings.com.au/90-x-45mm-framing-mgp12-h2-blue-pine-6-0m_p8031448"
tag = "p"
classname = "sc-cb9c4042-3 iGDFOw"

scraper = Scraper()
html = scraper.retrieve_html(url)
price = scraper.soup_finder(html, tag, classname)

print(price)
