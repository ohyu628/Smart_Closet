import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

# 데이터프레임을 저장할 리스트 생성
dataframes = []

# 페이지 범위 설정
start_page = 1
end_page = 351

# 각 페이지를 돌면서 데이터 수집
for page in tqdm(range(start_page, end_page + 1), desc="Pages"):
    try:
        driver.get(f"https://www.musinsa.com/app/styles/lists?use_yn_360=&style_type=&brand=&tag_no=&display_cnt=100&list_kind=big&sort=NEWEST&page={page}")
        wait = WebDriverWait(driver, 10)
        product_list_locator = (By.CSS_SELECTOR, 'body > div.wrap > div.right_area > form > div.right_contents.hover_box > div > ul > li')

        # 1부터 100까지의 상품을 클릭하며 스타일 정보 가져오기
        for i in tqdm(range(1, 101), desc="Items", leave=False):
            try:
                product_selector = wait.until(EC.visibility_of_element_located(product_list_locator))
                product_selector = driver.find_element(By.CSS_SELECTOR, f'body > div.wrap > div.right_area > form > div.right_contents.hover_box > div > ul > li:nth-child({i})')
                product_selector.click()
                
                # 코디 정보를 담을 딕셔너리 생성
                cody_dic = {}
                
                # 코디 번호
                cody_dic['cody_id'] = driver.current_url.split('/')[-1].split('?')[0]
                
                # 스타일
                cody_dic['style'] = driver.find_element(By.CSS_SELECTOR, "#style_info > h2").text
                
                # 날짜 및 조회수 정보 추출
                date_text = driver.find_element(By.CSS_SELECTOR, "#style_info > p").text
                # 조회수 분리
                date_parts = date_text.split('|')
                view_count = date_parts[-1].strip().split()[-1]
                # 조회수 정보를 제거한 날짜 문자열 다시 조합
                new_date = '|'.join(date_parts[:-1]).strip()
                # 날짜 및 조회수 
                cody_dic['date'] = new_date
                cody_dic['view_count'] = int(view_count.replace(',', ''))
                
                # 해시태그
                cody_dic['hashtag'] = driver.find_element(By.CSS_SELECTOR, "#style_info > div.styling_tag > div").text
                
                # 모델 정보 추출
                model_text = driver.find_element(By.CSS_SELECTOR, "#style_info > div.styling_goods > div.model > p").text
                # 모델 이름, 키, 몸무게
                cody_dic['model_name'] = model_text.split('\n')[0]
                height_weight = model_text.split('\n')[1]
                height, weight = height_weight.split(',')
                cody_dic['height'] = height
                cody_dic['weight'] = weight

                # 범위 설정
                start_index = 1
                end_index = 5 
                # 착용상품 이름 및 사이즈 정보 추출
                for j in range(start_index, end_index + 1):
                    try:
                        brand_text = driver.find_element(By.CSS_SELECTOR, f"#style_info > div.styling_goods > div.gender-classification > div > div > div.styling_list.swiper-wrapper > div:nth-child({j}) > a.brand_item").text
                        cody_dic[f'item{j}'] = brand_text
                    except NoSuchElementException:
                        cody_dic[f'item{j}'] = None  # 해당 CSS 선택자가 없으면 Null 값으로 설정

                    try:
                        option_text = driver.find_element(By.CSS_SELECTOR, f"#style_info > div.styling_goods > div.gender-classification > div > div > div.styling_list.swiper-wrapper > div:nth-child({j}) > span.option").text
                        cody_dic[f'item_size{j}'] = option_text
                    except NoSuchElementException:
                        cody_dic[f'item_size{j}'] = None  # 해당 CSS 선택자가 없으면 Null 값으로 설정

                
                # 데이터프레임으로 변환하여 리스트에 추가
                df = pd.DataFrame([cody_dic])
                dataframes.append(df)
                
                # 이전 페이지로 돌아가기
                driver.back()
                
            except Exception as e:
                print(f"Error occurred: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")
        break

# 리스트에 있는 모든 데이터프레임을 하나로 합치기
result_df = pd.concat(dataframes, ignore_index=True)
# CSV 파일로 저장
result_df.to_csv('/Users/ubin/playdata/vscode/crawling/musinsa/cody_info.csv', index=False)