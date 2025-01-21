from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
import xml.etree.ElementTree as ET

# .env 파일 로드
load_dotenv()

# 환경 변수에서 서비스 키 가져오기
SERVICE_KEY = os.getenv("SERVICE_KEY")

app = Flask(__name__)

# API 요청 함수
def get_bus_data(airport_code):
    url = "http://openapi.airport.co.kr/service/rest/AirportBusInfo/businfo"
    params = {
        "ServiceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "schAirport": airport_code
    }

    res = requests.get(url, params=params)
    if res.status_code == 200:
        root = ET.fromstring(res.text)
        bus_data = []

        for item in root.findall(".//item"):
            bus_data.append({
                "bus_category": item.find("busCategoryKorName").text if item.find("busCategoryKorName") is not None else "N/A",
                "bus_number": item.find("busDataBusNum").text if item.find("busDataBusNum") is not None else "N/A",
                "first_time": item.find("busDataFirstTime").text if item.find("busDataFirstTime") is not None else "N/A",
                "end_time": item.find("busDataEndTime").text if item.find("busDataEndTime") is not None else "N/A",
                "fare": item.find("busDataMoney").text if item.find("busDataMoney") is not None else "N/A",
                "route": item.find("busDataRouteKor").text if item.find("busDataRouteKor") is not None else "N/A",
                "stops": item.find("busDataEtcKor").text if item.find("busDataEtcKor") is not None else "N/A"
            })
        return bus_data
    else:
        return []

# 메인 페이지 라우트
@app.route("/")
def index():
    airports = {
        "CJJ": "청주",
        "TAE": "대구",
        "PUS": "김해",
        "GMP": "김포",
        "KUV": "군산",
        "KWJ": "광주",
        "CJU": "제주",
        "MWX": "무안",
        "HIN": "사천",
        "WJU": "원주",
        "YNY": "양양",
        "RSU": "여수"
    }
    return render_template("index.html", airports=airports)

# 공항별 시간표 라우트
@app.route("/schedule/<airport_code>")
def schedule(airport_code):
    bus_data = get_bus_data(airport_code)
    airport_name = {
        "CJJ": "청주",
        "TAE": "대구",
        "PUS": "김해",
        "GMP": "김포",
        "KUV": "군산",
        "KWJ": "광주",
        "CJU": "제주",
        "MWX": "무안",
        "HIN": "사천",
        "WJU": "원주",
        "YNY": "양양",
        "RSU": "여수"
    }.get(airport_code, "알 수 없는 공항")
    return render_template("schedule.html", airport_name=airport_name, bus_data=bus_data)

if __name__ == "__main__":
    app.run(debug=True)
