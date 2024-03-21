# 모듈
import pandas as pd
from tqdm import tqdm

# 파일 경로
dataset_path = "/.csv"

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(dataset_path)


# 컬럼별로 유의미한 전처리 시작

## 두께 thickness ##

# 대체할 문자열과 대체될 문자열을 딕셔너리로 정의합니다.
thickness_mapping = {
    '약간 얇음  보통': '약간 얇음, 보통',
    '보통  약간 두꺼움': '보통, 약간 두꺼움',
    '약간 두꺼움  두꺼움': '약간 두꺼움, 두꺼움',
    '얇음  약간 얇음': '얇음, 약간 얇음',
    '얇음  약간 얇음  보통': '얇음, 약간 얇음, 보통',
    '약간 얇음  보통  약간 두꺼움': '약간 얇음, 보통, 약간 두꺼움',
    '얇음  약간 얇음  보통  약간 두꺼움  두꺼움': '얇음, 약간 얇음, 보통, 약간 두꺼움, 두꺼움',
    '보통  약간 두꺼움  두꺼움': '보통, 약간 두꺼움, 두꺼움'
}

# 'thickness' 열에 있는 값을 대체합니다.
df['thickness'] = df['thickness'].replace(thickness_mapping)

# 'None' 값을 '약간 얇음, 보통'으로 대체합니다.
df['thickness'].fillna('약간 얇음, 보통', inplace=True)



## 성별 gender ##

# 결측치 제거
df = df.dropna(subset=['gender'])
# 값을 변환
df['gender'] = df['gender'].replace({'남성  여성': '남여공용', '상품구분  병행수입': '병행수입', 'None': '남여공용'})



## 시즌 Season ##

# category_small_name에 대한 season 대표값 설정
season_mapping = {
    '후드 티셔츠': '봄,가을,겨울',
    '반소매 티셔츠': '여름',
    '니트/스웨터': '겨울',
    '카디건': '봄,가을',
    '데님 팬츠': '봄,가을,겨울',
    "하의" : '봄,여름,가을,겨울',
    "베스트" : '봄,가을',
    "롱스커트" : '봄,가을',
    "트레이닝/조거 팬츠" : '봄,여름,가을,겨울',
    "트러커 재킷" : '봄,가을',
    "긴소매 티셔츠" : '봄,가을',
    "민소매 티셔츠" : '여름',
    "미니스커트" : '여름',
    "나일론/코치 재킷" : '봄,가을',
    "블루종/MA-1" : '봄,가을',
    "코튼 팬츠" : '봄,여름,가을,겨울',
    "스타디움 재킷" : '봄,가을',
    "슈트/블레이저 재킷" : '봄,여름,가을,겨울',
    "미디스커트" : '여름',
    "기타 상의" : '봄,여름,가을,겨울',
    "셔츠/블라우스" : '봄,여름,가을,겨울',
    "기타 아우터" : '봄,여름,가을,겨울',
    "피케/카라 티셔츠" : "봄,여름",
    "후드 집업" : "봄,가을",
    "겨울 싱글 코트" : "겨울",
    "사파리/헌팅 재킷" : '가을,겨울',
    "기타 바지" : '봄,여름,가을,겨울',
    "아우터" : '봄,가을,겨울',
    "환절기 코트" : '봄,가을',
    "상의" : '봄,여름,가을,겨울',
    "맨투맨/스웨트셔츠" : '봄,가을',
    "미니 원피스" : '봄,여름',
    "원피스" : '봄,여름,가을',
    "플리스/뽀글이" : '가을,겨울',
    "롱패딩/롱헤비 아우터" :'겨울',
    "숏패딩/숏헤비 아우터" :'겨울',
    "슈트 팬츠/슬랙스" : '봄,여름,가을,겨울',
    "패딩 베스트" : '겨울',
    "상하의세트" : '봄,여름,가을,겨울',
    "겨울 기타 코트" : '겨울',
    "미디 원피스" : '봄,여름,가을',
    "트레이닝 재킷" : '봄,가을',
    "겨울 더블 코트" :'겨울',
    "레깅스" : '봄,여름,가을,겨울',
    "스커트" : '봄,여름,가을,겨울',
    "점프 슈트/오버올" : '가을,겨울'
}

# category_small_name을 기반으로 season 결측치 채우기
df['season'] = df['season'].fillna(df['category_small_name'].map(season_mapping))

# 'season' 열의 값을 조건에 맞게 수정
df['season'] = df['season'].replace({'봄  여름  가을  겨울': '봄,여름,가을,겨울',
                                         '봄  가을  겨울': '봄,가을,겨울',
                                         '가을  겨울': '가을,겨울',
                                         '봄  여름  가을  겨울': '봄,여름,가을,겨울',
                                         '봄  여름  가을': '봄,여름,가을',
                                         '봄  가을': '봄,가을',
                                         '가을  겨울': '가을,겨울',
                                         '봄  여름': '봄,여름',
                                         '여름  가을': '여름,가을',
                                         '여름  가을  겨울': '여름,가을,겨울',
                                         '봄  겨울': '봄,겨울',
                                         '여름  가을  겨울': '여름,가을,겨울',
                                         '봄  여름  겨울': '봄,여름,겨울'})

# 'season' 열의 값을 조건에 맞게 수정
df['season'] = df['season'].replace({'None': '봄,여름,가을,겨울'})
# "봄, 여름, 가을, 겨울"에 해당하는 값들을 '봄,여름,가을,겨울'로 설정
df.loc[df['season'].isnull(), 'season'] = '봄,여름,가을,겨울'



## 패션시즌 fashion_season ##

# 'fashion_season' 열의 값을 수정
df['fashion_season'] = df['fashion_season'].str.replace(r'\d{4}\s*', '', regex=True)  # 연도 제거
df['fashion_season'] = df['fashion_season'].replace({'ALL ALL': 'ALL', '': None, 'ALL S/S': 'ALL', 'ALL F/W': 'ALL'})  # 'ALL ALL'을 'ALL'로 변경하고, 값이 없는 경우 None으로 변경, 'ALL S/S'와 'ALL F/W'를 'ALL'로 변경

# category_small_name 기준으로 fashion_season 결측치 매핑
fashion_season_mapping = {
    '맨투맨/스웨트셔츠': 'ALL',
    '니트/스웨터': 'F/W',
    '후드 티셔츠': 'ALL',
    '반소매 티셔츠': 'S/S',
    '긴소매 티셔츠': 'ALL',
    '셔츠/블라우스': 'ALL',
    '피케/카라 티셔츠': 'S/S',
    '기타 상의': 'ALL',
    '스포츠 상의': 'ALL',
    '민소매 티셔츠': 'S/S',
    '나일론/코치 재킷': 'ALL',
    '트러커 재킷': 'ALL',
    '스타디움 재킷': 'ALL',
    '기타 아우터': 'ALL',
    '블루종/MA-1': 'ALL',
    '사파리/헌팅 재킷': 'ALL',
    '슈트/블레이저 재킷': 'ALL',
    '레더/라이더스 재킷': 'ALL',
    '아노락 재킷': 'ALL',
    '숏패딩/숏헤비 아우터': 'F/W',
    '겨울 싱글 코트': 'F/W',
    '플리스/뽀글이': 'F/W',
    '겨울 기타 코트': 'F/W',
    '겨울 더블 코트': 'F/W',
    '무스탕/퍼': 'F/W',
    '롱패딩/롱헤비 아우터': 'F/W',
    '환절기 코트': 'ALL',
    '패딩 베스트': 'F/W',
    '트레이닝 재킷': 'ALL',
    '카디건': 'ALL',
    '후드 집업': 'ALL',
    '베스트': 'ALL',
    '데님 팬츠': 'ALL',
    '트레이닝/조거 팬츠': 'ALL',
    '코튼 팬츠': 'ALL',
    '슈트 팬츠/슬랙스': 'ALL',
    '기타 바지': 'ALL',
    '스포츠 하의': 'ALL',
    '숏 팬츠': 'S/S',
    '점프 슈트/오버올': 'ALL',
    '레깅스': 'ALL',
    '맥시 원피스': 'ALL',
    '미니 원피스': 'S/S',
    '미디 원피스': 'S/S',
    '미니스커트': 'S/S',
    '미디스커트': 'S/S',
    '롱스커트': 'ALL',
    '패션스니커즈화': 'ALL',
    '스포츠 스니커즈': 'ALL',
    '기타 스니커즈': 'ALL',
    '캔버스/단화': 'ALL',
    '로퍼': 'ALL',
    '힐/펌프스': 'ALL',
    '플랫 슈즈': 'ALL',
    '기타 신발': 'ALL',
    '블로퍼': 'ALL',
    '구두': 'ALL',
    '모카신/보트 슈즈': 'ALL',
    '부츠': 'ALL',
    '슬리퍼': 'ALL',
    '샌들': 'ALL',
    '신발 용품': 'ALL',
    '메신저/크로스 백': 'ALL',
    '숄더백': 'ALL',
    '백팩': 'ALL',
    '보스턴/드럼/더플백': 'ALL',
    '토트백': 'ALL',
    '웨이스트 백': 'ALL',
    '에코백': 'ALL',
    '브리프케이스': 'ALL',
    '클러치 백': 'ALL',
    '파우치 백': 'ALL',
    '지갑/머니클립': 'ALL',
    '가방 소품': 'ALL',
    '캐리어': 'ALL',
    '숄더백': 'ALL',
    '크로스백': 'ALL',
    '토트백': 'ALL',
    '백팩': 'ALL',
    '지갑/머니클립': 'ALL',
    '클러치 백': 'ALL',
    '웨이스트 백': 'ALL',
    '파우치 백': 'ALL',
    '가방 소품': 'ALL',
    '상의': 'ALL',
    '하의': 'ALL',
    '아우터': 'ALL',
    '상하의세트': 'ALL',
    '수영복/비치웨어': 'ALL',
    '스포츠잡화': 'ALL',
    '스포츠가방': 'ALL',
    '기구/용품/장비': 'ALL',
    '스포츠신발': 'ALL',
    '스포츠모자': 'ALL',
    '스커트': 'ALL',
    '원피스': 'ALL',
    '캠핑용품': 'ALL',
    '낚시용품': 'ALL',
    '캡/야구 모자': 'ALL',
    '비니': 'ALL',
    '페도라': 'ALL',
    '기타 모자': 'ALL',
    '버킷/사파리햇': 'ALL',
    '트루퍼': 'ALL',
    '헌팅캡/베레모': 'ALL',
    '양말': 'ALL',
    '스타킹': 'ALL',
    '셔츠/블라우스': 'ALL'
}

# 결측치 채우기
df['fashion_season'] = df['fashion_season'].fillna(df['category_small_name'].map(fashion_season_mapping))

# 'None'을 'ALL'로 대체
df['fashion_season'] = df['fashion_season'].replace('None', 'ALL')




## 비침도 Transparency ##

# 결측치 및 "None" 값 확인
missing_values = df['transparency'].isnull() | (df['transparency'] == 'None')

# 각 값의 비율 계산
value_counts = df['transparency'][~missing_values].value_counts(normalize=True)

# 결측치 및 "None" 값을 비율에 따라 채우기
df['transparency'] = df['transparency'].apply(lambda x: value_counts.idxmax() if pd.isnull(x) or x == 'None' else x)

# 다시 결측치 확인
missing_values = df['transparency'].isnull()

# 비율에 맞게 결측치 채우기
df.loc[missing_values, 'transparency'] = df.loc[missing_values, 'transparency'].apply(lambda x: value_counts.idxmax() if pd.isnull(x) else x)

# 각 값의 첫 번째와 두 번째 단어 추출
df['transparency'] = df['transparency'].apply(lambda x: ' '.join(x.split()[:2]))

# '보통 거의'를 '보통'으로 변경
df['transparency'] = df['transparency'].apply(lambda x: '보통' if '보통' in x else x)




## 해쉬태그 hashtag ##

for i in tqdm(range(df.shape[0])):
    if str(df['hashtag'].iloc[i]) == 'nan':
        df['hashtag'].iloc[i] = df['brand_name'].iloc[i] + ',' + df['category_big_name'].iloc[i] + ',' + df['category_small_name'].iloc[i]





## 소재 material ##
for i in tqdm(range(df.shape[0])):
    if df['category_small_name'].iloc[i] == '슈트/블레이저 재킷' and df['material'].iloc[i] == None:
        df['material'].iloc[i] = 'COTTON 100%'
    elif df['category_small_name'].iloc[i] == '슈트/블레이저 재킷' and str(df['material'].iloc[i]) == '상단표기':
        df['material'].iloc[i] = 'COTTON 100%'
    elif df['category_small_name'].iloc[i] == '슈트/블레이저 재킷' and str(df['material'].iloc[i]) == '상세설명  참조':
        df['material'].iloc[i] = 'POLYESTER 100%'
    elif df['category_small_name'].iloc[i] == '슈트/블레이저 재킷' and str(df['material'].iloc[i]) == '면  100%':
        df['material'].iloc[i] = 'COTTON 100%'
    elif df['category_small_name'].iloc[i] == '슈트/블레이저 재킷' and df['material'].iloc[i].__len__() > 17:
        df['material'].iloc[i] = 'POLYESTER 100%'

# 'material' 열에서 다양한 표현을 'COTTON 100%'로 통일
df['material'] = df['material'].replace({'COTTON  100%': 'COTTON 100%', 'Cotton  100%': 'COTTON 100%', 'COTTON 100%': 'COTTON 100%'})
df['material'] = df['material'].replace({'100%  코튼': 'COTTON 100%'})

# 'material' 열에서 패턴에 따라 값을 변경
df['material'] = df['material'].replace({
    'COTTON  100%': 'COTTON 100%',
    'Cotton  100%': 'COTTON 100%',
    'COTTON 100%': 'COTTON 100%',
    '100%  코튼': 'COTTON 100%',
    '면|cotton': 'COTTON 100%',
    'POLYESTER 100% 100%': 'POLYESTER 100%',  # 수정된 부분
    'POLYESTER|폴리에스터': 'POLYESTER 100%',
    'None': 'POLYESTER 100%'  # 'None' 값이 'POLYESTER 100%'로 변경됩니다.
}, regex=True)

# 'material' 열에서 '겉감  :  COTTON 100%  100%' 값을 'COTTON 100%'로 대체
df['material'] = df['material'].replace({'겉감  :  COTTON 100%  100%.': 'COTTON 100%'})

# 'material' 열에서 '상품  상세설명  참조'를 '상세설명참조'로 대체
df['material'] = df['material'].replace({'상품  상세설명  참조': '상세설명참조'})

# 'POLYESTER 100%' 중복 확인
polyester_100_rows = df['material'].str.contains('POLYESTER 100%', na=False)
df.loc[polyester_100_rows, 'material'] = 'POLYESTER 100%'

# 'COTTON 100%' 중복 확인
cotton_100_rows = df['material'].str.contains('COTTON 100%100%', na=False)
df.loc[cotton_100_rows, 'material'] = 'COTTON 100%'

# 'COTTON 100%' 중복 확인
cotton_100_rows = df['material'].str.contains('코튼  100%', na=False)
df.loc[cotton_100_rows, 'material'] = 'COTTON 100%'

# 'COTTON'을 포함하는 모든 값을 'COTTON 100%'로 대체
df['material'] = df['material'].replace({r'.*COTTON.*': 'COTTON 100%'}, regex=True)

# '상세설명참조'를 '상세페이지참조'로 변경
df['material'] = df['material'].replace({'폴리  100%': 'POLYESTER 100%'})

# '상세설명참조'를 '상세페이지참조'로 변경
df['material'] = df['material'].replace({'상세설명참조': '상세페이지참조'})

# '상세설명참조'를 '상세페이지참조'로 변경
df['material'] = df['material'].replace({'상세이미지  참조': '상세페이지참조'})

# '상세설명참조'를 '상세페이지참조'로 변경
df['material'] = df['material'].replace({'[상세설명참조]': '상세페이지참조'})

df['material'] = df['material'].replace({
    'Wool  100%': 'WOOL  100%',
    'WOOl  100%': 'WOOL  100%',
    'wool  100%': 'WOOL  100%',
    '울  100% ': 'WOOL  100%',
    '울60%폴리40%': 'WOOL  100%',
    '울60%  폴리40%': 'WOOL  100%',
    '울100%': 'WOOL  100%',
    '상세설명참조': '상세페이지참조',
    '폴리67  레이온22  울8': 'POLYESTER 100%',
    '리넨  100%': 'LINEN 100%',
    '울  100%': 'WOOL  100%',
    'POLY  100%': 'POLYESTER 100%',
    '상세이미지참조': '상세페이지참조'
})




## 색상 color ##

# 'color' 열에서 '상세'를 포함하는 값들을 필터링하여 출력
df_detail = df[df['color'].str.contains('상세|KC인증', na=False)]

# df_detail에 해당하는 고유한 값들을 데이터프레임으로 변환
df_detail_values = pd.DataFrame(df_detail['color'].unique(), columns=['color'])

# detail_values에서 제외할 값들
excluded_values = ['BEIGE', 'BLACK', 'CHARCOAL', 'BROWN', 'KHAKI']

# 제외할 값들을 포함하는 행을 제외한 나머지 값을 추출하여 데이터프레임 생성
filtered_df_detail_values = df_detail_values[~df_detail_values['color'].str.contains('|'.join(excluded_values))]

for value in filtered_df_detail_values['color']:
    df.loc[df['color'] == value, 'color'] = 'NONE'

df['color'] = df['color'].str.replace('COLOR', '', regex=True)
df['color'] = df['color'].str.replace(r'[^a-zA-Z0-9가-힣\s]', '', regex=True)
df['color'] = df['color'].str.replace(r'\s+', '', regex=True)
df['color'] = df['color'].str.replace(r'\d+', '', regex=True)

# NaN 값을 'Unknown'으로 대체
df['color'] = df['color'].fillna('Unknown')

# 'color' 열에서 각 색상을 포함하는 값들을 변경
df.loc[df['color'].str.contains('블랙|검정|BLK0|BLK|ZBBLACK|블|BK|BLACKBLACK|INK', case=False), 'color'] = 'BLACK'
df.loc[df['color'].str.contains('빨강|레드|빨간', case=False), 'color'] = 'RED'
df.loc[df['color'].str.contains('화이트|흰색|OFFWHITE|GNSWHS|OWHITE|WHWHITE|색상WHT', case=False), 'color'] = 'WHITE'
df.loc[df['color'].str.contains('네이비|남색|DARKNAVY|색상NVY', case=False), 'color'] = 'NAVY'
df.loc[df['color'].str.contains('베이지|LIGHTBEIGE|DARKBEIGE|ECRU', case=False), 'color'] = 'BEIGE'
df.loc[df['color'].str.contains('그레이|회색|LIGHTGREY|DARKGREY|GY|LGREY', case=False), 'color'] = 'GRAY'
df.loc[df['color'].str.contains('블루|파랑|파란|OPENBLUE|SBLUE|BLUESTRIPE', case=False), 'color'] = 'BLUE'
df.loc[df['color'].str.contains('카키|LIGHTKHAKI|FORESTKHAKI', case=False), 'color'] = 'KHAKI'
df.loc[df['color'].str.contains('브라운|갈색|DARKBROWN', case=False), 'color'] = 'BROWN'
df.loc[df['color'].str.contains('초록|녹색|그린|DARKGREEN|연두', case=False), 'color'] = 'GREEN'
df.loc[df['color'].str.contains('핑크|분홍|LIGHTPINK|소라', case=False), 'color'] = 'PINK'
df.loc[df['color'].str.contains('하늘|SKY|LIGHTBLUE|SEA', case=False), 'color'] = 'SKYBLUE'
df.loc[df['color'].str.contains('LIGHTPASTELBLUE', case=False), 'color'] = 'PASTELBLUE'
df.loc[df['color'].str.contains('아이보리', case=False), 'color'] = 'IVORY'
df.loc[df['color'].str.contains('크림', case=False), 'color'] = 'CREAM'
df.loc[df['color'].str.contains('오렌지|DARKORANGE', case=False), 'color'] = 'ORANGE'
df.loc[df['color'].str.contains('차콜', case=False), 'color'] = 'CHARCOAL'
df.loc[df['color'].str.contains('옐로우|노랑|레몬', case=False), 'color'] = 'YELLOW'
df.loc[df['color'].str.contains('올리브', case=False), 'color'] = 'OLIVE'
df.loc[df['color'].str.contains('민트', case=False), 'color'] = 'MINT'
df.loc[df['color'].str.contains('퍼플', case=False), 'color'] = 'PURPLE'
df.loc[df['color'].str.contains('라벤다', case=False), 'color'] = 'LAVENDER'
df.loc[df['color'].str.contains('DARKVANILLA', case=False), 'color'] = 'VANILLA'
df.loc[df['color'].str.contains('카멜', case=False), 'color'] = 'CAMEL'
df.loc[df['color'].str.contains('라임', case=False), 'color'] = 'LIME'
df.loc[df['color'].str.contains('자주|와인', case=False), 'color'] = 'WINE'
df.loc[df['color'].str.contains('버건디', case=False), 'color'] = 'BURGUNDY'

# 'color' 열의 데이터에 대해 일부 한국어 색상을 영어로 매핑
color_mapping = {
    "BLACKWHITE": 'BLACK,WHITE',
    "WHITEBLACK": 'BLACK,WHITE',
    "BLCKWHTE": 'BLACK,WHITE',
    "MELANGEGREY": "MELANGE, REY",
    "BEIGEKHAKI": "BEIGE,KHAKI",
    "BEIGEBLACK": "BLACK,BEIGE",
    "BLACKIVORY": "BLACK,IVORY",
    "IVORYBLACK": "BLACK,IVORY",
    "BLACKCHARCOAL": "BLACK,CHARCOAL",
    "BLACKKHAKI": "BLACK,KHAKI",
    "BLACKBROWN": 'BLACK,BROWN',
    "BLACKCREAM": "BLACK,CREAM",
    "IVORYBEIGE": "IVORY,BEIGE",
    "BLUEGRAY": "BLUE,GRAY",
    "설명페이지참조": "NONE",
    "멀티컬러": "NONE",
    "STRIPE": "NONE",
    "스트라이프": "NONE",
    "NAVYWHTE입고시기에따라정보가상이할수있어수령하신상품의라벨을참고하시기바랍니다": "NAVY,WHITE",
    "BLCKWHTE입고시기에따라정보가상이할수있어수령하신상품의라벨을참고하시기바랍니다": 'BLACK,WHITE',
    "NAVYBROWNWINEINDIGOIVORY": "NAVY,BROWN,WINE",
}

# 'color' 열의 각 원소에 대해 매핑된 값으로 새로운 열 추가
df['color'] = df['color'].map(color_mapping).fillna(df['color'])
threshold = 3  # 임계값 설정

# value_counts를 사용하여 각 색상의 빈도수를 계산하고, 개수가 threshold보다 작은 것을 필터링하여 가져옵니다.
colors_to_exclude = df['color'].value_counts()[df['color'].value_counts() <= threshold].index

# 'color' 열의 값이 colors_to_exclude에 포함되어 있는 경우에만 'NONE'으로 변경합니다.
df.loc[df['color'].isin(colors_to_exclude), 'color'] = 'NONE'

