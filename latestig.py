# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 12:10:56 2020

@author: user
"""
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

driver = webdriver.Chrome(executable_path=r'C:\Users\user\Desktop\chromedriver.exe')
driver.get('https://www.instagram.com/manchesterunited')


driver.find_element_by_xpath('// button[@class="sqdOP  L3NKy   y3zKF     "]').click()
time.sleep(3)
driver.find_element_by_xpath('// input[@name="username"]').send_keys('gigilulu6')
time.sleep(3)
driver.find_element_by_xpath('// input[@name="password"]').send_keys('Gigilulu@6')
time.sleep(3)
driver.find_element_by_xpath('// button[@type="submit"]').click()
time.sleep(3)
driver.find_element_by_xpath('// button[@class="sqdOP yWX7d    y3zKF     "]').click()
time.sleep(3)

Pagelength = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
links=[]
source = driver.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.string.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
#try 'script.string' instead of script.text if you get error on index out of range
for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
    links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')


result=pd.DataFrame()
for i in range(len(links)):
 try:
  page = urlopen(links[i]).read()
  data = bs(page, 'html.parser')
  body = data.find('body')
  script = body.find('script')
  raw = script.string.strip().replace('window._sharedData =', '').replace(';', '')
  json_data=json.loads(raw)
  posts =json_data['entry_data']['PostPage'][0]['graphql']
  posts= json.dumps(posts)
  posts = json.loads(posts)
  x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
  x.columns = x.columns.str.replace('shortcode_media.', '')
  result=result.append(x)
 except:
  np.nan
  

result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))

post = ['_typename','display_url','edge_media_to_parent_comment.count','edge_media_preview_like.count']

result = result.loc[:, result.columns.isin(post)]

result.to_csv('result.csv', index=True)
