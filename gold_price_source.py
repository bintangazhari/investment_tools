from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
import pandas as pd
import re


def web_driver():

  options = webdriver.ChromeOptions()
  options.add_argument("--verbose")
  options.add_argument('--no-sandbox')
  options.add_argument('--headless')
  options.add_argument('--disable-gpu')
  options.add_argument("--window-size=1920, 1200")
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=options)
  return driver

def sellprice_antam():
  driver = web_driver()
  driver.get('https://www.logammulia.com/id/harga-emas-hari-ini')
  size = []
  price = []

  table = driver.find_elements(By.XPATH, '/html/body/section[3]/div/div[3]/div/div[1]/table[1]/tbody')
  for data in table:
    _text = data.find_elements(By.TAG_NAME, "td")
    for i in range (0,36):
      if i==0 or i%3==0:
        size.append(_text[i].text)
      elif i%3==1:
        price.append((_text[i].text))

  antam_table = pd.DataFrame(list(zip(size, price)),
                columns =['Size (gr)', 'Price'])
  antam_table['Size (gr)'] = pd.to_numeric(antam_table['Size (gr)'].str.replace(' gr',''))
  antam_table['Price'] = pd.to_numeric(antam_table['Price'].str.replace(',',''), downcast = 'integer')
  antam_table['Source'] = "Antam"
  antam_table['date'] = date.today()
  return antam_table

def buyback_antam():
  driver = web_driver()
  driver.get('https://www.logammulia.com/id/sell/gold')
  buyback_price = driver.find_element(By.XPATH, '/html/body/section[3]/div/div/div[2]/div/div/div[2]/div/div[1]/span[2]/span[2]').text
  buyback_price = buyback_price.replace("Rp ","")
  buyback_price = int(buyback_price.replace(",",""))
  return buyback_price

def price_antam():
  antam_table = sellprice_antam()
  antam_table['Buyback'] = pd.to_numeric(buyback_antam()*antam_table['Size (gr)'], downcast = 'integer')
  return antam_table


def sellprice_lotus():
  driver = web_driver()
  driver.get('https://lotusarchi.com/pricing/')
  size = []
  price = []
  table = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/table/tbody')
  _list = table.find_elements(By.TAG_NAME, "tr")
  for i in range(11):
    _row = _list[i].find_elements(By.TAG_NAME, "td")
    _size = _row[0].text
    _price = _row[1].text
    size.append(_size.split()[0])
    price.append(_price)
  lotus_table = pd.DataFrame(list(zip(size, price)),
                columns =['Size (gr)', 'Price'])
  lotus_table['Size (gr)'] = pd.to_numeric(lotus_table['Size (gr)'])
  lotus_table['Price'] = pd.to_numeric(lotus_table['Price'].str.replace(',',''), downcast = 'integer')
  lotus_table['Source'] = "Lotus Archi"
  lotus_table['date'] = date.today()
  lotus_table.drop_duplicates(inplace=True)
  return lotus_table


def buyback_lotus():
  driver = web_driver()
  driver.get('https://lotusarchi.com/pricing/')
  buyback_price = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/h4/strong[2]').text
  buyback_price = re.search(r'[0-9\.]+', buyback_price)
  buyback_price = int(buyback_price.group().replace(".",""))
  return buyback_price

def price_lotus():
  lotus_table = sellprice_lotus()
  lotus_table['Buyback'] = pd.to_numeric(buyback_lotus()*lotus_table['Size (gr)'], downcast = 'integer')
  return lotus_table

