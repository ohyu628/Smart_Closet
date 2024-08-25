import pandas as pd
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import mysql.connector
from airflow.models import XCom
import json
from sqlalchemy import create_engine
from sqlalchemy import text
from selenium.common.exceptions import NoSuchElementException
from airflow.operators.bash_operator import BashOperator


# MySQL 연결 설정
config = {
    "user": "[사용자]",
    "password": "[비밀번호]",
    "host": "[퍼블릭 ip]",
    "database": "[데이터베이스]",
    "port": "3306"
}

# DAG 설정
dag = DAG(
    dag_id='cody_test5',
    schedule_interval='0 1 * * *',  # 매일 01시에 실행
    start_date=datetime.now(),
)

# 데이터베이스에서 cody_id를 추출하여 CSV 파일로 저장하는 함수
def extract_existing_cody_ids():
    # 데이터베이스 연결
    conn = mysql.connector.connect(**config)
    print("Connected to the database successfully.")
    cursor = conn.cursor()
        
    # 기존에 저장된 cody_id 가져오기
    sql = "SELECT cody_id FROM Cody"
    cursor.execute(sql) 
    existing_cody_ids = [row[0] for row in cursor.fetchall()]

    # 데이터프레임으로 변환
    df = pd.DataFrame(existing_cody_ids, columns=['cody_id'])
    
    # 데이터프레임을 CSV 파일로 저장
    if os.path.isdir("./cody_test") == False:
        os.mkdir("./cody_test")

    if os.path.isfile('./cody_test/cody_id.csv') == False:
        df.to_csv('./cody_test/cody_id.csv', index=False)

    print(df)

# PythonOperator를 사용하여 함수 실행
cody_test_DB = PythonOperator(task_id='extract_existing_cody_ids',
                        python_callable=extract_existing_cody_ids,
                        dag=dag
)

def extract_new_product_info(existing_cody_ids):
    # ChromeOptions 객체 생성
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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="122.0.6261.94").install()), options=options)

    # 데이터를 저장할 리스트 생성
    data_list = []

    # 페이지 로드
    for page_num in range(1, 5): 
        driver.get(f"https://www.musinsa.com/app/styles/lists?use_yn_360=&style_type=&brand=&tag_no=&display_cnt=100&list_kind=big&sort=NEWEST&page={page_num}")
        # 대기 시간 설정
        wait = WebDriverWait(driver, 10)

        # 페이지 로드를 대기하기 위한 조건 설정
        product_list_locator = (By.CSS_SELECTOR, 'body > div.wrap > div.right_area > form > div.right_contents.hover_box > div > ul > li')

        # 각 페이지의 상품을 클릭하며 스타일 정보 가져오기
        for i in range(1, 100):
            try:
                # 페이지 로드를 대기
                product_selector = wait.until(EC.visibility_of_element_located(product_list_locator))
                # 각 상품 요소에 대한 CSS 선택자
                product_selector = driver.find_element(By.CSS_SELECTOR, f'body > div.wrap > div.right_area > form > div.right_contents.hover_box > div > ul > li:nth-child({i})')
                # 해당 상품 클릭
                product_selector.click()
                
                # 코디 정보를 담을 딕셔너리 생성
                cody_dic = {}
                
                # 현재 페이지의 URL에서 상품 번호만 추출하여 JSON 파일명 생성
                cody_id = driver.current_url.split('/')[-1].split('?')[0]
                
                # 기존에 저장된 cody_id와 비교하여 새로운 데이터인지 확인
                if cody_id not in existing_cody_ids:
                    # 스타일 정보 추출 및 저장
                    cody_dic['cody_id'] = cody_id
                    cody_dic['style'] = driver.find_element(By.CSS_SELECTOR, "#style_info > h2").text
                    
                    # 날짜 및 조회 정보 추출
                    date_text = driver.find_element(By.CSS_SELECTOR, "#style_info > p").text
                    date_parts = date_text.split('|')
                    view_count = date_parts[-1].strip().split()[-1]
                    new_date = '|'.join(date_parts[:-1]).strip()
                    cody_dic['date'] = new_date
                    cody_dic['view_count'] = int(view_count.replace(',', ''))
                    
                    # 해시태그 정보 추출 및 저장
                    cody_dic['hashtag'] = driver.find_element(By.CSS_SELECTOR, "#style_info > div.styling_tag > div").text
                    
                    # 모델 정보 추출
                    model_text = driver.find_element(By.CSS_SELECTOR, "#style_info > div.styling_goods > div.model > p").text
                    cody_dic['model_name'] = model_text.split('\n')[0]
                    height_weight = model_text.split('\n')[1]
                    height, weight = height_weight.split(',')
                    cody_dic['height'] = height
                    cody_dic['weight'] = weight

                    # 범위 설정
                    start_index = 1
                    end_index = 5

                    # 브랜드 정보 및 옵션 정보 추출
                    for i in range(start_index, end_index + 1):
                        try:
                            brand_text = driver.find_element(By.CSS_SELECTOR, f"#style_info > div.styling_goods > div.gender-classification > div > div > div.styling_list.swiper-wrapper > div:nth-child({i}) > a.brand_item").text
                            cody_dic[f'item{i}'] = brand_text
                        except NoSuchElementException:
                            cody_dic[f'item{i}'] = None  # 해당 CSS 선택자가 없으면 Null 값으로 설정

                        try:
                            option_text = driver.find_element(By.CSS_SELECTOR, f"#style_info > div.styling_goods > div.gender-classification > div > div > div.styling_list.swiper-wrapper > div:nth-child({i}) > span.option").text
                            cody_dic[f'item_size{i}'] = option_text
                        except NoSuchElementException:
                            cody_dic[f'item_size{i}'] = None  # 해당 CSS 선택자가 없으면 Null 값으로 설정

                    # 데이터를 리스트에 추가
                    data_list.append(cody_dic)

                # 이전 페이지로 돌아가기
                driver.back()
                
            except Exception as e:
                print(f"Error occurred: {e}")

    # 데이터를 담은 리스트 반환
    return data_list

# PythonOperator를 사용하여 함수 실행
extract_new_product_info_task = PythonOperator(task_id='extract_new_product_info',
                                                python_callable=extract_new_product_info,
                                                op_kwargs={'existing_cody_ids': '{{ ti.xcom_pull(task_ids="extract_existing_cody_ids") }}'},
                                                provide_context=True,
                                                dag=dag
)

# 데이터베이스 연결 정보 설정
db_connection = 'mysql+mysqlconnector://teamdb:1234@43.200.110.68:3306/teamdata'

# 데이터를 데이터베이스에 저장하는 함수 정의
def save_data_to_database(**kwargs):
    data_list = kwargs['ti'].xcom_pull(task_ids='extract_new_product_info')
    engine = create_engine(db_connection)
    for data in data_list:
        try:
            # '#'을 제거합니다.
            if 'hashtag' in data:
                data['hashtag'] = data['hashtag'].replace('#', '')

            # 데이터베이스에 저장
            with engine.connect() as connection:
                with connection.begin():
                    connection.execute(
                        text(
                            """
                            INSERT INTO Cody_New (cody_id, style, date, view_count, hashtag, model_name, height, weight, item1, item_size1, item2, item_size2, item3, item_size3, item4, item_size4, item5, item_size5) 
                            VALUES (:cody_id, :style, :date, :view_count, :hashtag, :model_name, :height, :weight, :item1, :item_size1, :item2, :item_size2, :item3, :item_size3, :item4, :item_size4, :item5, :item_size5)
                            """
                        ),
                        **data
                    )
        except Exception as e:
            print(f"Error occurred while saving data: {str(e)}")

save_data_task = PythonOperator(
    task_id='save_data_to_database_task',
    python_callable=save_data_to_database,
    provide_context=True,
    dag=dag
)

remove_file = BashOperator(
    task_id="remove_file", 
    bash_command="rm -f ./cody_test/cody_id.csv", 
    dag=dag
)

cody_test_DB >> extract_new_product_info_task >> save_data_task >> remove_file
