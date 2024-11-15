# 🧣 오늘모입지
> '오늘모입지'는 옷장에 방치되어 있는 옷들을 의류 폐기물로 만들지 않기 위해, 스마트 옷장에 사진을 등록하면 어떤 종류의 의류인지 분류하고 원하는 스타일에 맞게 코디를 추천해주는 웹 서비스입니다.
<br/>

## Team
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/whatevereyewant"><img src="https://avatars.githubusercontent.com/u/145940008?v=4" width="100px;" alt=""/><br /><sub><b>김수아</b></sub></a><br /><sub><b>백엔드</b></sub><br /></td>
      <td align="center"><a href="https://github.com/suddy78"><img src="https://avatars.githubusercontent.com/u/113496210?v=4" width="100px;" alt=""/><br /><sub><b>김수연</b></sub></a><br /><sub><b>모델</b></sub><br /></td>
      <td align="center"><a href="https://github.com/jmeagnes"><img src="https://avatars.githubusercontent.com/u/151423959?v=4" width="100px;" alt=""/><br /><sub><b>정모은</b></sub></a><br /><sub><b>모델</b></sub><br /></td>
      <td align="center"><a href="https://github.com/jiminchur"><img src="https://avatars.githubusercontent.com/u/145955453?v=4" width="100px;" alt=""/><br /><sub><b>지민철</b></sub></a><br /><sub><b>데이터엔지니어(팀장)</b></sub><br /></td>
      <td align="center"><a href="https://github.com/ohyu628"><img src="https://avatars.githubusercontent.com/u/154876483?v=4" width="100px;" alt=""/><br /><sub><b>오유빈</b></sub></a><br /><sub><b>데이터엔지니어</b></sub><br /></td>
      <td align="center"><a href="https://github.com/jaechoi97"><img src="https://avatars.githubusercontent.com/u/145918829?v=4" width="100px;" alt=""/><br /><sub><b>최재웅</b></sub></a><br /><sub><b>데이터분석</b></sub><br /></td>
    </tr>
  </tbody>
</table>
<br/>
<br/>

## 1. 프로젝트 개요
[문제현상]

> 요즘 패스트푸드처럼 최신 유행을 즉각 반영하여 저렴함 가격으로 제작, 유통함으로써 상품 회전율을 빠르게하여 일명 패스트패션으로 불리고 있습니다. 옷장에 무엇이 있는지 기억도 못한채 다시 옷을 구입하게 되어 불필요한 소비를 하게 되는 악순환이 반복되며, 통계청에 따르면 2021년 하루 기준 약 575톤 이상의 의류 폐기물이 발생하였고 현시점에는 더욱 증가하였을 것이라고 예상됩니다.
<br/>

[솔루션]
> 고객의 옷을 스마트 옷장에 등록함으로써 개인화된 추천 시스템을 구축하여 고객의 취향에 맞게 옷을 추천해 줌으로써 자신이 가지고 있는 옷을 활용하여 불필요한 소비를 하지 않도록 하여 보다 적은 의류 폐기물이 발생하도록 합니다.

> 본 프로젝트는 사용자의 선호도, 외출목적, 날씨를 고려한 맞춤형 코디 추천과 스마트 옷장 관리를 위한 웹 서비스를 목표로 하고 있습니다.
<br/>

## 2. 기획 및 개발 일정 (WBS)
> 기획 및 설계, 백엔드, 모델, 엔지니어, 분석 6가지 카테고리로 Task를 구분짓고 일정을 할당하였습니다.
>
[요구분석 명세서](https://docs.google.com/document/d/1GnTlrJgWTk3o4aaLqI1ZXnLC5DrBan0ntmjrJnWubdo/edit)

[WBS](https://docs.google.com/spreadsheets/d/1FakvPad7NTO7V1t1Nr_8PB-BNMYLDHi1/edit#gid=1543558811)
<br/>
<br/>
<br/>

## 3. 개발
### 기술스택
**Web**<br>
<img src="https://img.shields.io/badge/springboot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

**Model**<br>
<img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black">
<img src="https://img.shields.io/badge/aws rekognition-569A31?style=for-the-badge&logo=&logoColor=black">

**Data**<br>
<img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=black">
<img src="https://img.shields.io/badge/airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=black">
<img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=black">
<img src="https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=black">

**ETC**<br>
<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
<img src="https://img.shields.io/badge/ec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=black">
<img src="https://img.shields.io/badge/apigateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=black">
<img src="https://img.shields.io/badge/lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=black">
<img src="https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=black">
<img src="https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=black">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=black">
<img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=black">

**Communication**<br>
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white">
<br/>
<br/>
<br/>



### 시스템 아키텍처
![아키텍처](/img/아키텍처.png)
<br/>
<br/>


### 데이터 파이프라인
> 무신사 웹사이트에서 필요한 데이터를 JSON 파일로 추출한 후, Apache Airflow를 통해 전처리와 표준화를 거쳐 데이터베이스에 저장하는 과정을 자동화했습니다.

![파이프라인](/img/데이터파이프라인.png)
<br/>
<br/>
<br/>

### Lambda와 AWS APIGateway로 모델 서빙
![아키텍처](/img/webserving01.png)
<br/>
<br/>
<br/>

## 4. 발표자료
![image](https://github.com/user-attachments/assets/3718fcda-5eae-46e7-9daa-1919f56e0a3a)
[오늘모입지_발표자료.pdf](https://github.com/user-attachments/files/16828950/default.pdf)


