import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# 셀레니움
options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

prefs = {"profile.managed_default_content_settings.images": 2,
         "profile.managed_default_content_settings.javascript": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

df = pd.read_csv('~/musinsa/product_id.csv')
small_code_lst = df['category_small_code'].tolist()[44:47] # 이 부분 수정 인덱싱 <<<<<<<<<<<
category_small_code = small_code_lst[0][1:]

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

for n in tqdm(range(len(small_code_lst))):
    # 소분류 카테고리 코드
    category_small_code = small_code_lst[n][1:]
    
    df_ = pd.read_csv(f'~/musinsa/product_code/{category_small_code}.csv')
    _df_lst = df_['product_code'].tolist()

    for product_code in tqdm(_df_lst):
        product_code = product_code[1:]
    
        url = f'https://www.musinsa.com/app/goods/{product_code}'
        while True:
            try:
                driver.get(url)
                break
            except:
                print("웹드라이버 오류")
                driver.quit()
                driver = webdriver.Chrome(options=options)
    
        # 1 상품 주요 정보    
        try:
            tmp = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.jdxLyK > div.product-detail__sc-8631sn-1.edxTcD > div.product-detail__sc-8631sn-4.fMixbN > div.product-detail__sc-achptn-0.eXRtIE > ul")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'li'):
                lst.append(i.text.split('\n'))
            save_to_json({product_code: lst}, f"./information/{product_code}.json")
        except:
            pass
            
        # 2 상품 재질 정보
        all_dic = {}
        try:
            table = driver.find_element(By.CSS_SELECTOR, '#root > div.product-detail__sc-8631sn-0.jdxLyK > div.product-detail__sc-8631sn-1.edxTcD > div.product-detail__sc-8631sn-3.sFcvA > div.product-detail__sc-17fds8k-0.dtRkwA')
            target_color = 'rgba(0, 0, 0, 1)'
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                lst_g = row.text
                lst_sample = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td') if cell.value_of_css_property('color') == target_color]
                lst_a = lst_g.split(' ')
                all_dic[lst_a[0]] = lst_sample
            save_to_json({product_code: all_dic}, f"./infor/{product_code}.json")
        except:
            pass
    
        # 3 해시태그
        try :
            tmp = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.jdxLyK > div.product-detail__sc-8631sn-1.edxTcD > div.product-detail__sc-8631sn-4.fMixbN > div.product-detail__sc-achptn-0.eXRtIE > div")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'a'):
                lst.append(i.text)
            if len(lst) != 0:
                save_to_json({product_code: lst}, f"./hastag/{product_code}.json")
        except :
            pass
    
        # 4 상품정보 제공고시
        try :
            tmp = driver.find_element(By.CSS_SELECTOR, "#rootBottom > section.product-detail__sc-99ltlm-0.kzjnpk > table")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'tr')[1:]:
                lst.append(i.text.split(' '))
            save_to_json({product_code: lst}, f"./infor_extra/{product_code}.json")
        except :
            pass
    
        # 5 상세페이지 이미지
        try :
            table = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(3) > section.product-detail__sc-5zi22l-0.tACkg")
            imgs = [img.get_attribute('src') for img in table.find_elements(By.TAG_NAME, 'img')]
            save_to_json({product_code: {'infor_img': imgs}}, f"./infor_img/{product_code}.json")
        except:
            pass
        

        # 6 가격
        try :
            tmp = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.jdxLyK > div.product-detail__sc-8631sn-1.edxTcD > div.product-detail__sc-8631sn-4.fMixbN > div.product-detail__sc-w5wkld-0.jdBwFu > div.product-detail__sc-1p1ulhg-0.hauxDp")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'li'):
                lst.append(i.text.split('\n'))
            save_to_json({product_code: lst}, f"./price/{product_code}.json")
        except:
            pass