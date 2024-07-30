import time
from datetime import date
import pandas as pd
import re
from gold_price_source import *

def money_exchange():
  _amount = []
  _price = []
  _source = []
  _date = []
  _buyback = []

  driver = web_driver()
  driver.get('https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/default.aspx')
  _kurs_table = driver.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_GridView1"]/table/tbody')
  _row_table = _kurs_table.find_elements(By.TAG_NAME,"tr")
  for i in range(len(_row_table)):
    _row_table_info = _row_table[i].find_elements(By.TAG_NAME, "td")
    currency = _row_table_info[0].text
    amount = int(_row_table_info[1].text)
    sell_price = int(_row_table_info[2].text.replace(",","").replace(".",""))/100
    buyback_price = int(_row_table_info[3].text.replace(",","").replace(".",""))/100
    _amount.append(amount)
    _price.append(sell_price)
    _source.append(currency)
    _date.append(date.today())
    _buyback.append(buyback_price)
  data = {
      'Amount': _amount,
      'Price': _price,
      'Source': _source,
      'date': _date,
      'Buyback': _buyback
  }
  currency_table = pd.DataFrame.from_dict(data)
  return currency_table