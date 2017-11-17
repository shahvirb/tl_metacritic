import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

QUERY_URL = "https://www.torrentleech.org/torrents/browse/index/categories/17/facets/category%253AGames_subcategory%253APC"

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query):
    driver.get(QUERY_URL)
    html = driver.page_source
    parse_html(html)
    

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    #time.sleep(5)
    driver.quit()