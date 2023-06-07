from django.shortcuts import render
import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta
from urllib.parse import urlencode, quote_plus, unquote
import json,math

import googlemaps
import os
# Create your views here.

def index(request):

    NX = 149  ## X축 격자점 수
    NY = 253  ## Y축 격자점 수

    Re = 6371.00877  ##  지도반경
    grid = 5.0  ##  격자간격 (km)
    slat1 = 30.0  ##  표준위도 1
    slat2 = 60.0  ##  표준위도 2
    olon = 126.0  ##  기준점 경도
    olat = 38.0  ##  기준점 위도
    xo = 210 / grid  ##  기준점 X좌표
    yo = 675 / grid  ##  기준점 Y좌표
    first = 0

    if first == 0:
        PI = math.asin(1.0) * 2.0
        DEGRAD = PI / 180.0
        RADDEG = 180.0 / PI

        re = Re / grid
        slat1 = slat1 * DEGRAD
        slat2 = slat2 * DEGRAD
        olon = olon * DEGRAD
        olat = olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        first = 1

    def mapToGrid(lat, lon, code=0):
        ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = lon * DEGRAD - olon
        if theta > PI:
            theta -= 2.0 * PI
        if theta < -PI:
            theta += 2.0 * PI
        theta *= sn
        x = (ra * math.sin(theta)) + xo
        y = (ro - ra * math.cos(theta)) + yo
        x = int(x + 1.5)
        y = int(y + 1.5)
        return x, y

    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCrtPDz8CRxIql6iBEVhvUXPBlgvdXrJdY'
    data = {
        'considerIp': True,
        'cellTowers': [],
    }
    result = requests.post(url, data)

    loca = result.json().get('location').get('lat')
    loca1 = result.json().get('location').get('lng')

    url2 = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    key = '8vmL%2FmpOsG19eWY%2Bbvi609ZBBMV%2FJ65TfFSy2M80l28%2BY5lDEy0Rm3fbglBrJEl51wWmC8s3RMetgEjgG0DKgw%3D%3D'

    serviceKeyDecoded = unquote(key, 'UTF-8')

    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")

    season = "봄"
    todate = int(datetime.today().strftime("%m"))

    if 3 <= todate <= 5:
        season = "봄"
    elif 6 <= todate <= 8:
        season = "여름"
    elif 9 <= todate <= 11:
        season = "가을"
    elif datetime.today().strftime("%m") == 12:
        season = "겨울"
    elif 1 <= todate <= 2:
        season = "겨울"

    if now.minute < 45:  # base_time와 base_date 구하는 함수
        if now.hour == 0:
            base_time = "2330"
            base_date = yesterday
        else:
            pre_hour = now.hour - 1
            if pre_hour < 10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
            base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
        base_date = today

    base_date1 = base_date
    astime = base_time

    if 2 >= now.hour >= 0:
        base_date1 = yesterday

    if 3 <= now.hour < 10:
        astime = "0" + str(now.hour) + "00"
    elif 0 <= now.hour <= 2:
        astime = "0300"
    else:
        astime = str(now.hour) + "00"

    nx, ny = mapToGrid(loca, loca1)

    queryParams = '?' + urlencode({quote_plus('serviceKey') : serviceKeyDecoded,
                                   quote_plus('pageNo') : '1', quote_plus('base_date') : base_date,
                                   quote_plus('base_time') : base_time, quote_plus('nx') : nx, quote_plus('ny') : ny,
                                   quote_plus('dataType') : 'json', quote_plus('numOfRows') : '1000'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey') : serviceKeyDecoded,
                                   quote_plus('pageNo') : '1', quote_plus('base_date') : base_date1,
                                   quote_plus('base_time') : '0200', quote_plus('nx') : nx, quote_plus('ny') : ny,
                                   quote_plus('dataType') : 'json', quote_plus('numOfRows') : '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = base_date

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['obsrValue']
        # 습도
        if item['category'] == 'REH':
            weather_data['reh'] = item['obsrValue']
        # 1시간 동안 강수량
        if item['category'] == 'RN1':
            weather_data['rain'] = item['obsrValue']

    data2 = dict()
    data2['date'] = base_date

    weather_data2 = dict()
    for item in items2['item']:
        #오늘 아침에 준 데이터
        #강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == base_date1:
                if item['fcstTime'] == astime:
                    weather_data2['pop'] = item['fcstValue']
        #하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == base_date1:
                if item['fcstTime'] == astime:
                    weather_data2['sky'] = item['fcstValue']
        #최저기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == base_date1:
                if item['fcstTime'] == '0600':
                    weather_data2['tmn'] = item['fcstValue']
        #최고기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == base_date1:
                if item['fcstTime'] == '1500':
                    weather_data2['tmx'] = item['fcstValue']
    seoul = 0
    if season == "봄":
        seoul = 1
    elif season == "여름":
        seoul = 2
    elif season == "가을":
        seoul = 3
    elif season == "겨울":
        seoul = 4

    return render(request, 'index.html', {'tmp': weather_data['tmp'], 'reh': weather_data['reh'], 'rain': weather_data['rain'],'pop': weather_data2['pop'],'sky': weather_data2['sky'],
                                          'tmx':weather_data2['tmx'], 'tmn':weather_data2['tmn'], 'seoul':seoul
                                          })



