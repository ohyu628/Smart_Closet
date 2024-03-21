import os
import requests 
import pandas as pd
import time
import requests
from sqlalchemy import create_engine
from airflow import DAG 
from airflow.operators.python import PythonOperator
import warnings
from datetime import datetime
import mysql.connector
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from webdriver_manager.chrome import ChromeDriverManager
from airflow.operators.bash_operator import BashOperator
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from airflow import DAG
warnings.filterwarnings("ignore")

# MySQL 연결 설정
config = {
    "user": "id",
    "password": "pw",
    "host": "ip address",
    "database": "database",
    "port": "3306"
}

# 스케줄링
default_start_date = datetime(2024, 3, 19)

dag = DAG(
    dag_id='product',
    schedule_interval='0 1 * * *', # 매일 새벽 1시에 실행
    start_date=default_start_date,
    catchup=False, # 과거 기간에 대한 실행을 방지
)


# category_small_code에 대한 데이터프레임 생성 
def product_fetch_and_create_dataframe():
    # MySQL 데이터베이스 연결 및 커서 생성
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # SQL 쿼리 실행
    sql = "SELECT category_small_code FROM CategorySmall;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    # 컬럼 이름 추출 및 소문자 변환
    colname = cursor.description
    col = [i[0].lower() for i in colname]
    
    # 데이터프레임 생성
    df_product_ = pd.DataFrame(rows, columns=col)
    
    # 'test' 디렉토리 없으면 생성
    if not os.path.isdir("./test"):
        os.mkdir("./test")
    
    # 'df_product.csv' 파일 없으면 생성 및 데이터프레임 저장
    file_path = './test/df_product.csv'
    if not os.path.isfile(file_path):
        df_product_.to_csv(file_path, index=False, encoding='utf-8')

    # 데이터베이스 연결 종료
    cursor.close()
    conn.close()

# 에어플로우 PythonOperator 설정
product_fetch_data_task = PythonOperator(
    task_id='make_df_product_',
    python_callable=product_fetch_and_create_dataframe,                                 
    dag=dag
)

def get_soup(url):
    try:
        response = requests.get(url)
        if response.status_code == 403:
            time.sleep(300) # 재시도 전 대기
            response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        print(f"Error occurred: {e}")
    return None



# 새로운 상품 리스트 
def scrape_musinsa():
    df_product_ = pd.read_csv('./test/df_product.csv', encoding='utf-8')
    lst = []
    BASE_URL = 'https://www.musinsa.com/categories/item/'
    for code in df_product_['category_small_code'].str[1:]:
        page = 1
        url = f"{BASE_URL}{code}?d_cat_cd={code}&list_kind=small&sort=new&page={page}&display_cnt=90"
        soup = get_soup(url)
        if soup:
            products = soup.select('a.img-block')
            for product in products:
                try:
                    product_id = product['href'].split("/")[-1]
                    product_name = product['title']
                    img_url = product.select_one('img.lazyload.lazy')['data-original']
                    brand = product.select_one('img.lazyload.lazy')['alt'].split(" ")[0]
                    lst.append({
                        'category_small_code': 'B' + code,
                        'product_code': 'C' + product_id,
                        'product_name': product_name,
                        'product_img_url': img_url,
                        'brand_name': brand
                    })
                except Exception as e:
                    print(f"Error extracting product info: {e}")
                    continue
    df_save = pd.DataFrame(lst)
    df_save.to_csv('./test/df_save.csv', index=False, encoding='utf-8')
    
    # DB 연결 정보를 환경 변수로부터 가져오는 것이 좋습니다.
    engine = create_engine('mysql+mysqlconnector://id:password@ip address:3306/database')
    df_save.to_sql(name='ProductCode', con=engine, if_exists='append', index=False)

scrape_musinsa_task = PythonOperator(task_id='scrape_musinsa',
                                     python_callable=scrape_musinsa,
                                     dag=dag)

def setup_webdriver():
    # 셀레니움
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="122.0.6261.94").install()), options=options)

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def create_directories():
    directories = ["./infor", "./information", "./infor_extra", "./price"]
    for directory in directories:
        if not os.path.isdir(directory):
            os.mkdir(directory)



def product_crawling():
    df_save = pd.read_csv('./test/df_save.csv', encoding='utf-8')
    product_codes = df_save['product_code'].tolist()[:10]

    create_directories()
    
    driver = setup_webdriver()

    for product_code in product_codes:
        product_code = product_code[1:]
        print(product_code)
        url = f'https://www.musinsa.com/app/goods/{product_code}'
        print(url)
        try:
            driver.get(url)
        except Exception as e:
            print("웹드라이버 오류:", e)
            continue

    
        # 1 상품 주요 정보  #
        try:
            tmp = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-4.goIKhx > div.product-detail__sc-achptn-0.bHXxTQ > ul")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'li'):
                lst.append(i.text.split('\n'))
            save_to_json({product_code: lst}, f"./information/{product_code}.json")
            print("상품 주요 정보 수집 성공")
        except Exception as e:
            print("상품 주요 정보 수집 실패:", e)

                
        # 2 상품 재질 정보 #
        all_dic = {}
        try:
            table = driver.find_element(By.CSS_SELECTOR, '#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-17fds8k-0.PpQGA')
            target_color = 'rgba(0, 0, 0, 1)'
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                lst_g = row.text
                lst_sample = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td') if cell.value_of_css_property('color') == target_color]
                lst_a = lst_g.split(' ')
                all_dic[lst_a[0]] = lst_sample
            save_to_json({product_code: all_dic}, f"./infor/{product_code}.json")
            print("상품 재질 정보 수집 성공")
        except Exception as e:
            print("상품 재질 정보 수집 실패:", e)


        # 4 상품정보 제공고시 #
        try :
            tmp = driver.find_element(By.CSS_SELECTOR, "#rootBottom > section.product-detail__sc-99ltlm-0.bcUgsM > table")
            lst = []
            for i in tmp.find_elements(By.TAG_NAME, 'tr')[1:]:
                lst.append(i.text.split(' '))
            save_to_json({product_code: lst}, f"./infor_extra/{product_code}.json")
            print("상품정보 제공고시 수집 성공")
        except Exception as e:
            print("상품정보 제공고시 수집 실패:", e)

        # 6 가격 #
        try :
            tmp = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-4.goIKhx > div.product-detail__sc-w5wkld-0.hgCYZm > div.product-detail__sc-1p1ulhg-0.jEclp")
            lst = []                                    
            for i in tmp.find_elements(By.TAG_NAME, 'li'):
                lst.append(i.text.split('\n'))
            save_to_json({product_code: lst}, f"./price/{product_code}.json")
            print("가격 정보 수집 성공")
        except Exception as e:
            print("가격 정보 수집 실패:", e)
    driver.quit()

product_crawling_task = PythonOperator(task_id='product_crawling',
                                    python_callable=product_crawling,
                                    dag=dag)

def read_json_files(directory):
    dic = []
    for file in os.listdir(directory):
        if file.endswith('.json'):
            with open(os.path.join(directory, file), 'r') as f:
                data = json.load(f)
                dic.extend([[key, value] for key, value in data.items()])
    return pd.DataFrame(dic)


def data_processing():
    # JSON 파일 읽기
    dfs = {name: read_json_files(f'./{name}/') for name in [ 'infor_extra', 'information', 'price']}
    
    # 컬럼 이름 설정 및 데이터프레임 병합
    rename_dict = {'infor_extra': 'infor_extra', 'information': 'information', 'price': 'price2'}
    for name, df in dfs.items():
        df.columns = ['product_code', rename_dict[name]]
    df_merged = pd.concat(dfs.values(), axis=1).loc[:,~pd.concat(dfs.values(), axis=1).columns.duplicated()]


    df_merged[['fit','texture','elasticity','transparency','thickness','season',
    'material','color','size','fashion_season','gender',
    'view_1month','sales_1year','likes',
    'review_rating','review','price']] = None


    # product_code
    df_merged['product_code'] = 'C' + df_merged['product_code']

    # infor_extra
    df_merged['material'] = df_merged['infor_extra'].apply(lambda x: str(x[0][2:]).strip('[]').replace("'", '') if len(x) > 0 else None)
    df_merged['color'] = df_merged['infor_extra'].apply(lambda x: str(x[1][1:]).strip('[]').replace("'", '') if len(x) > 1 else None)
    df_merged['size'] = df_merged['infor_extra'].apply(lambda x: str(x[2][1:]).strip('[]').replace("'", '') if len(x) > 2 else None)

    # price
    df_merged['price'] = df_merged['price2'].apply(lambda x: int(x[0][1][:-1].replace(',', '')) if len(x) > 0 else None)

    # infor
    for feature, eng_feature in zip(['핏', '촉감', '신축성', '비침', '두께', '계절'], 
                                ['fit', 'texture', 'elasticity', 'transparency', 'thickness', 'season']):
        df_merged[eng_feature] = df_merged['infor'].apply(lambda x: str(x.get(feature, '')).strip('[]').replace("'", ''))


    # information
    def process_information(row):
        for k in row:
            if '시즌' in k and '성별' in k:
                return k[2].split(' ')[-1], k[3]
            elif '성별' in k:
                return None, k[1]
        return None, None  # 기타 조건도 적절히 추가

    df_merged[['fashion_season', 'gender']] = df_merged['information'].apply(lambda x: pd.Series(process_information(x)))


    drop_cols = ['infor_extra', 'information','price2']

    df_merged.drop(drop_cols,axis=1,inplace=True)

    engine = create_engine('mysql+mysqlconnector://id:password@ip address:3306/database')
    for i in range(df_merged.shape[0]):
        try :
            df_merged.iloc[i].to_sql(name='ProductInfo', con=engine, if_exists='append', index=False)  # 추후에 컬럼 설정과 테이블 변경이 이루어져야함
        except Exception as e:
            print(e)
            continue

data_processing_task = PythonOperator(task_id='data_processing',
                                    python_callable=data_processing,
                                    dag=dag)

remove_file = BashOperator(
    task_id="remove_file", bash_command="rm -rf ./infor ./information ./infor_extra ./price", dag=dag
)



product_fetch_data_task >> scrape_musinsa_task >> product_crawling_task >> data_processing_task >> remove_file

