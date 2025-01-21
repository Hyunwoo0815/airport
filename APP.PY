from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 공항 코드와 이름 매핑
AIRPORTS = {
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

# API 요청 함수
def get_bus_data(airport_code):
    url = "http://openapi.airport.co.kr/service/rest/AirportBusInfo/businfo"
    params = {
        "ServiceKey": "WKp1VvR7awnciw/bWZyS/ucpv8Tiihgn8LgHK7a7Hw0u+ewXMZNo7buPDOywQc2k7pjJssVL39S0Oe6RWzCa3w==",
        "pageNo": 1,
        "numOfRows": 100,
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
    return render_template("index.html", airports=AIRPORTS)

# 공항별 시간표 라우트
@app.route("/schedule/<airport_code>")
def schedule(airport_code):
    airport_name = AIRPORTS.get(airport_code, "알 수 없음")
    bus_data = get_bus_data(airport_code)  # API 호출 및 데이터 가져오기
    return render_template("schedule.html", airport_code=airport_code, airport_name=airport_name, bus_data=bus_data)

if __name__ == "__main__":
    app.run(debug=True)
