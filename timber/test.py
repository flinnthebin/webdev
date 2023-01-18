##!/usr/bin/python3

import re
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
  
  def soup_finder(self, html: str, tag: str, classname: str, regex: str) -> str:
    # make the soup
    soup = BeautifulSoup(html, 'lxml')
    # find the tag and class in the html, regex to search for price, strip whitespace and `-` chars
    price = re.search(regex, soup.find(tag, class_=classname).text).group().strip(" -")
    return price

b_url = "https://www.bunnings.com.au/90-x-45mm-framing-mgp10-h2-blue-pine-6-0m_p8031034"
b_tag = "p"
b_classname = "sc-cb9c4042-3 iGDFOw"
b_regex = r'\$\d+\.\d+'

bj_url = "https://www.barrenjoeytimber.com.au/structural-pine-mpg10"
bj_tag = "div"
bj_classname = "dmNewParagraph u_1696189223"
bj_regex = r'\$\d+\.\d+'

c_url = "https://canterburytimbers.com.au/buy/h2-timber-treated-pine-mgp10-90-x-45/"
c_tag = "span"
c_classname = "price price--withTax"
c_regex = r'\s-\s\$\d+\.\d+'


scraper = Scraper()
html = scraper.retrieve_html(c_url)
price = scraper.soup_finder(html, c_tag, c_classname, c_regex)

print(price)
