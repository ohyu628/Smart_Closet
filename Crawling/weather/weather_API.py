import requests

# OpenWeatherMap API 키를 여기에 입력하세요
api_key = '공유한 API 키 입력'

# 날씨 정보를 가져올 도시와 국가 코드
city = 'Seoul'
country_code = 'KR'

# OpenWeatherMap API 엔드포인트 URL
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

# API 요청 및 응답 받기
response = requests.get(url)
weather_data = response.json()