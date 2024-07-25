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
                columns =['Amount', 'Price'])
  antam_table['Amount'] = pd.to_numeric(antam_table['Amount'].str.replace(' gr',''))
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
  antam_table['Buyback'] = pd.to_numeric(buyback_antam()*antam_table['Amount'], downcast = 'integer')
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
                columns =['Amount', 'Price'])
  lotus_table['Amount'] = pd.to_numeric(lotus_table['Amount'])
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
  lotus_table['Buyback'] = pd.to_numeric(buyback_lotus()*lotus_table['Amount'], downcast = 'integer')
  return lotus_table

def usd_to_idr():
  driver = web_driver()
  driver.get('https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/default.aspx')
  _kurs_table = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_GridView1"]/table/tbody')
  _row_table = _kurs_table.find_elements(By.TAG_NAME,"tr")
  _row_table_info = _row_table[23].find_elements(By.TAG_NAME, "td")
  sell_price = int(_row_table_info[2].text.replace(",","").replace(".",""))/100
  buyback_price = int(_row_table_info[3].text.replace(",","").replace(".",""))/100
  data = {
      'Amount': [1],
      'Price': [sell_price],
      'Source': ["Bank Indonesia"],
      'date': [date.today()],
      'Buyback': [buyback_price]
  }
  usd_table = pd.DataFrame.from_dict(data)
  return usd_table
  

