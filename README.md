# 오늘모입지??
> Encore Dataengineering 28기 부트캠프 final project

# Team
지민철 오유빈 김수연 정모은 김수아 최재웅 

# Use Tech
### Web
<!-- <div align=center>  -->
<img src="https://img.shields.io/badge/springboot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
<!-- </div> -->

### Model
<!-- <div align=center> -->
<img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black">
<img src="https://img.shields.io/badge/aws rekognition-569A31?style=for-the-badge&logo=&logoColor=black">
<!-- </div> -->

### Data
<!-- <div align=center> -->
<img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=black">
<img src="https://img.shields.io/badge/airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=black">
<img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=black">
<img src="https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=black">
<!-- </div> -->

### ETC
<!-- <div align=center> -->
<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
<img src="https://img.shields.io/badge/ec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=black">
<img src="https://img.shields.io/badge/apigateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=black">
<img src="https://img.shields.io/badge/lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=black">
<img src="https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=black">
<img src="https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=black">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=black">
<img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=black">
<!-- </div> -->

### Communication
<!-- <div align=center> -->
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white">
<!-- </div> -->

# 전체 프로젝트 일정
* 프로젝트 일정 : 2024.02.19 ~ 2024.03.22

# 목차
* [프로젝트 개요](##프로젝트-개요)
* [요구분석명세서](#요구분석-명세서)
* [WBS](#wbs)
* [데이터 파이프라인](#데이터-파이프라인)
* [데이터 모니터링](#데이터-모니터링)
* [Lambda와 AWS APIGateway로 모델 서빙](#lambda와-aws-apigateway로-모델-서빙)
* [전체적인 아키텍처](#전체적인-아키텍처)
* [회고](#회고)

## 프로젝트 개요
요즘 패스트푸드처럼 최신 유행을 즉각 반영하여 저렴한 가격으로 제작, 유통함으로써 상품 회전율을 빠르게하여 일명 패스트패션으로 불리고 있다. 옷장에 무엇이 있는지 기억도 못한채 다시 옷을 구입하게 되어 불필요한 소비를 하게 되는 악순환을 반복하고 있다. 통계청에 따르면 2021년 하루 기준 약 575톤 이상의 의류 폐기물이 발생하였고, 현시점에는 더욱 증가하였을 것이라 예상된다. 이러한 문제점을 해결할 필요성을 느껴 옷장 및 옷 코디 추천 페이지(오늘모입지)를 고안하게 되었다. 이 프로젝트는 사용자의 선호도, 외출목적, 날씨를 고려한 맞춤형 코디 추천과 스마트 옷장 관리를 위한 웹 어플리케이션 제작을 목표로 한다.

## 요구분석 명세서
* [링크](https://docs.google.com/document/d/1GnTlrJgWTk3o4aaLqI1ZXnLC5DrBan0ntmjrJnWubdo/edit#heading=h.xwas7dkx0kjw)
## WBS
![wbs](/img/wbs.png)
## 데이터 파이프라인
![파이프라인](/img/데이터파이프라인.png)
### [이슈링크 (1)](https://github.com/jiminchur/Recommend-Model_Closet-Cody/issues/4)
### [이슈링크 (2)](https://github.com/jiminchur/Recommend-Model_Closet-Cody/issues/5)
## 데이터 모니터링
![모니터링](/img/모니터링.png)
### [이슈링크 (1)](https://github.com/jiminchur/Recommend-Model_Closet-Cody/issues/12)
## Lambda와 AWS APIGateway로 모델 서빙
![아키텍처](/img/webserving01.png)
### [이슈링크 (1)](https://github.com/jiminchur/Recommend-Model_Closet-Cody/issues/18)
* Lambda test (성공)
![lambda](/img/ppt_lambda-test.gif)
* /predict test (성공)
![lambda](/img/ppt_-_predict-test%20(1).gif)
* endpoint url test (성공)
![lambda](/img/ppt_endpoint-url-test.gif)
## 전체적인 아키텍처
![아키텍처](/img/아키텍처.png)
## 회고
> 이번 프로젝트에서 ETL 처리 자동화 구축, 모니터링 시스템 구현, 그리고 서버리스 아키텍처를 활용한 모델 서빙까지 성공적으로 달성했다. 이 모든 과정은 스마트 옷장 구현을 위한 중요한 발판이었던것같다. 특히, 코디 추천 기능을 서비스에 통합하려는 계획이 있었으나, 일정 관리 문제로 인해 그 부분을 실현하지 못한 것은 아쉬운 점으로 남는다. 과거에 추천 모델을 포함한 프로젝트를 진행한 경험이 있어 이번에도 순조롭게 적용할 수 있을 것이라 기대했으나, 실제로는 그러지 못했다. 그럼에도 불구하고, 팀원 간의 원활한 커뮤니케이션과 여러 차례의 회의를 통해 기능을 조정하여 스마트 옷장의 핵심 기능만을 구현한 것은 긍정적인 성과라 할 수 있었다. 이를 통해 우리 팀은 유연성과 협업의 중요성을 다시 한번 깨닫게 되었던거 같다.




