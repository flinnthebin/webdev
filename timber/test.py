#!/usr/bin/python3

import logging
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# configure the logging module
# TODO: structure logging to time-series to as to provide 1Y min format
logging.basicConfig(filename="scraper.log", level=logging.ERROR)

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
      price = re.search(regex, soup.find(tag, class_=classname).text).group().strip(" $-")
      return price
  
    # not functioning correctly - bugfix
    # scraper has no object attribute "soup_finder_all"
    def soup_finder_all(self, html: str, tag: str, classname: str, regex: str) -> str:
      # make the soup
      soup = BeautifulSoup(html, 'lxml')
      # find all elements matching the tag and class
      elements = soup.find_all(tag, class_=classname)
      if elements:
        for element in elements:
          match = re.search(regex, element.text)
          if match:
            price = match.group().strip(" $-")
            return price
      else:
            return None


suppliers = {
    "Barrenjoey Timber": {
        "url": "https://www.barrenjoeytimber.com.au/structural-pine-mpg10",
        "tag": "div",
        "classname": "dmNewParagraph u_1696189223",
        "regex": r'\$\d+\.\d+',
        "unit": "lm"
    },
    "Bunnings": {
        "url": "https://www.bunnings.com.au/90-x-45mm-framing-mgp10-h2-blue-pine-3-9m_p8031027",
        "tag": "p",
        "classname": "sc-ef11ce11-3 kiVfla",
        "regex": r'\$\d+\.\d+',
        "unit": 3.9
    },
    "Canterbury Timber": {
        "url": "https://canterburytimbers.com.au/buy/h2-timber-treated-pine-mgp10-90-x-45/",
        "tag": "span",
        "classname": "price price--withTax",
        "regex": r'\s-\s\$\d+\.\d+',
        "unit": 6.0
    },
    "Blacktown Building Supplies": {
        "url": "https://www.blacktownbuildingsupplies.com.au/product/structural-pine-h2-termite-treated-mgp10-90-x-45/",
        "tag": "span",
        "classname": "woocommerce-Price-amount amount",
        "regex": r'\d+.\d+',
        "unit": 6.0
    }
}

scraper = Scraper()

for supplier in suppliers:
  url = suppliers[supplier]["url"]
  tag = suppliers[supplier]["tag"]
  classname = suppliers[supplier]["classname"]
  regex = suppliers[supplier]["regex"]
  unit = suppliers[supplier]["unit"]

  html = scraper.retrieve_html(url)
  try:
    price = float(scraper.soup_finder_all(html, tag, classname, regex))
    if unit != 6.0:
      if unit == "lm":
        price = price * 6.0
      else:
        price = price / unit * 6.0
    print(f"The price at {supplier} is ${round(price,2)}")
  except AttributeError as e:
    # log the error message
    logging.error(f"Error: Incorrect link or unable to find specified tag and class for {supplier} - {e}")