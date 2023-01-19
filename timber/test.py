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

suppliers = {
    "Barrenjoey Timber": {
        "url": "https://www.barrenjoeytimber.com.au/structural-pine-mpg10",
        "tag": "div",
        "classname": "dmNewParagraph u_1696189223",
        "regex": r'\$\d+\.\d+'
    },
    "Bunnings": {
        "url": "https://www.bunnings.com.au/90-x-45mm-framing-mgp10-h2-blue-pine-6-0m_p8031034",
        "tag": "p",
        "classname": "sc-cb9c4042-3 iGDFOw",
        "regex": r'\$\d+\.\d+'
    },
    "Canterbury Timber": {
        "url": "https://canterburytimbers.com.au/buy/h2-timber-treated-pine-mgp10-90-x-45/",
        "tag": "span",
        "classname": "price price--withTax",
        "regex": r'\s-\s\$\d+\.\d+'
    }
}

scraper = Scraper()

for supplier in suppliers:
  url = suppliers[supplier]["url"]
  tag = suppliers[supplier]["tag"]
  classname = suppliers[supplier]["classname"]
  regex = suppliers[supplier]["regex"]

  html = scraper.retrieve_html(url)
  try:
    price = scraper.soup_finder(html, tag, classname, regex)
    print(f"The price at {supplier} is {price}")
  except AttributeError:
    print(f"Error: Incorrect link or unable to find specified tag and class for {supplier}")
    continue
