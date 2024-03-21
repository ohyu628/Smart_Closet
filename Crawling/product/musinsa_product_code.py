import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv('~/musinsa/product_id.csv')
df2 = df[['category_small_code','category_small_page_count']]

def get_url(code, page):
    return f'https://www.musinsa.com/categories/item/{code}?d_cat_cd={code}brand=&list_kind=small&sort=new&sub_sort=&page={page}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='

def fetch_page(code, page):
    url = get_url(code, page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    if str(response).split(" ")[-1][1:4] == '403':
        print("ip 일시적인 차단")
        return []
    products = soup.select('a.img-block')
    lst = []
    for product in products:
        try :
            product_id = product['href'].split("/")[-1]
            product_name = product['title']
            img_url = product.select_one('img.lazyload.lazy')['data-original']
            brand = product.select_one('img.lazyload.lazy')['alt'].split(" ")[0]
            dic = {}
            dic['category_small_code'] = 'B' + code
            dic['product_code'] = 'C' + product_id
            dic['product_name'] = product_name
            dic['product_img_url'] = img_url
            dic['brand_name'] = brand
            lst.append(dic)
        except Exception as e:
            print(f"실패: {e}")
    return lst

def fetch_category(a):
    code,page = df2.iloc[a]
    code = code[1:]
    page = min(page, 400)
    lst = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_page, [code]*page, range(1,page + 1))
    for result in results:
        lst.extend(result)
    df_save = pd.DataFrame(lst)
    df_save.to_csv(f"~/musinsa/{code}.csv",index=False,encoding="utf-8-sig")

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(fetch_category, range(46,60)) # <<<< 인덱싱 수정 가능 구간
