import requests 
import pandas as pd
import FinanceDataReader as fdr
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import requests
from selenium.webdriver.common.by import By
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

category_dic = {
    '상의' : '001',
    '아우터' : '002',
    '바지' : '003',
    '원피스' : '020',
    '스커트' : '022',
    '스니커즈' : '018',
    '신발' : '005',
    '가방' : '004',
    '여자 가방' : '054',
    '스포츠 용품' : '017',
    '모자' : '007',
    '양말' : '008'
           }
category_lst = ['001','002','003','020','022','018','005','004','054','017','007','008']

def find_key_by_value(dictionary, value):
    return next((key for key, val in dictionary.items() if val == value), None)

lst_ = []

for l in tqdm(category_lst):
    url = f"https://www.musinsa.com/categories/item/{l}?d_cat_cd={l}&brand=&list_kind=small&sort=new&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    lst = soup.find_all('li',attrs={'data-filter-key':'d_cat_cd'})
    category = find_key_by_value(category_dic,l)
    for k in range(lst.__len__()) :
        dic_ = {}
        dic_['category_big_name'] = category
        dic_['category_big_code'] = 'A' + l
        category_name = soup.find_all('li',attrs={'data-filter-key':'d_cat_cd'})[k]['data-filter-text'].split(":")[-1].strip()
        category_code = soup.find_all('li',attrs={'data-filter-key':'d_cat_cd'})[k]['data-filter-value']
        dic_['category_small_name'] = category_name
        dic_['category_small_code'] = 'B' + category_code
        url = f'https://www.musinsa.com/categories/item/{category_code}?d_cat_cd={category_code}&brand=&list_kind=small&sort=new&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        page = int(str(soup.find_all('span', attrs={'class':'totalPagingNum'})[0]).split(">")[1].split("<")[0])
        dic_['category_small_page_count'] = page
        lst_.append(dic_)

df = pd.DataFrame(lst_)

df.to_csv(f"~/musinsa/product_id.csv",index=False,encoding="utf-8-sig")