from django.shortcuts import render
import requests
import requests # HTTP 요청을 보내는 모듈
from urllib.parse import urlencode, quote_plus, unquote
import json,math
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta
import os
# Create your views here.
today = datetime.today().strftime("%Y%m%d")
to = today + '0600'

d = date.today() + timedelta(days=2)
y = date.today() - timedelta(days=1)
t = date.today() + timedelta(days=1)
yesterday = y.strftime("%Y%m%d")
tomorrow = t.strftime("%Y%m%d")
dayafter = d.strftime("%Y%m%d")

if datetime.now().hour < 2:
    to = yesterday + '1800'
    dayafter = tomorrow
    tomorrow = today
    today = yesterday

url = "https://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
url2 = "https://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
url3 = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
key = '8vmL%2FmpOsG19eWY%2Bbvi609ZBBMV%2FJ65TfFSy2M80l28%2BY5lDEy0Rm3fbglBrJEl51wWmC8s3RMetgEjgG0DKgw%3D%3D'
serviceKeyDecoded = unquote(key, 'UTF-8')

def Seoul(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11B10101',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11B00000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 61, quote_plus('ny'): 126,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'seoul.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })
def Busan(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11H20201',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11H20000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 100, quote_plus('ny'): 76,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'busan.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })

def Incheon(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11B20201',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11B00000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 55, quote_plus('ny'): 124,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'incheon.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })


def Daegu(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11H10701',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11B00000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 89, quote_plus('ny'): 90,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'daegu.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })



def Daejeon(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11C20401',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11C20000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 67, quote_plus('ny'): 100,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'daejeon.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })



def Gwangju(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11H10701',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11F20000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 58, quote_plus('ny'): 74,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'gwangju.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })



def Ulsan(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11H20101',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11H20000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 102, quote_plus('ny'): 84,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'ulsan.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })



def Jeju(request):
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId') : '11G00201',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows') : '100'})

    queryParams2 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('tmFc'): to,
                                   quote_plus('pageNo'): '1', quote_plus('regId'): '11G00000',
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '100'})

    queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 52, quote_plus('ny'): 38,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})

    res = requests.get(url + queryParams, verify=False)
    res2 = requests.get(url2 + queryParams2, verify=False)
    res3 = requests.get(url3 + queryParams3, verify=False)

    items = res.json().get('response').get('body').get('items')
    items2 = res2.json().get('response').get('body').get('items')
    items3 = res3.json().get('response').get('body').get('items')

    data = dict()
    data['date'] = today

    weather_data = dict()
    #현재기온
    for item in items['item']:
        # 기온
        weather_data['min4'] = item['taMin4']
        weather_data['min5'] = item['taMin5']
        weather_data['min6'] = item['taMin6']
        weather_data['min7'] = item['taMin7']
        weather_data['max4'] = item['taMax4']
        weather_data['max5'] = item['taMax5']
        weather_data['max6'] = item['taMax6']
        weather_data['max7'] = item['taMax7']

    data2 = dict()
    data2['date'] = today

    weather_data2 = dict()
    # 현재기온
    for item in items2['item']:
        # 기온
        weather_data2['rnSt4Am'] = item['rnSt4Am']
        weather_data2['rnSt5Am'] = item['rnSt5Am']
        weather_data2['rnSt6Am'] = item['rnSt6Am']
        weather_data2['rnSt7Am'] = item['rnSt7Am']

        weather_data2['wf4Am'] = item['wf4Am']
        weather_data2['wf5Am'] = item['wf5Am']
        weather_data2['wf6Am'] = item['wf6Am']
        weather_data2['wf7Am'] = item['wf7Am']

    data3 = dict()
    data3['date'] = today

    weather_data3 = dict()
    # 현재기온
    for item in items3['item']:
        # 오늘 아침에 준 데이터
        # 강수확률
        if item['category'] == 'POP':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['pop1'] = item['fcstValue']
        # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['sky1'] = item['fcstValue']
        #기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn1'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == today:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx1'] = item['fcstValue']

        #내일
        if item['category'] == 'POP':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['pop2'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['sky2'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn2'] = item['fcstValue']
        #최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == tomorrow:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx2'] = item['fcstValue']

        # 2일후
        if item['category'] == 'POP':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['pop3'] = item['fcstValue']
            # 하늘 상태  1 맑음  3. 구름많음  4. 흐림
        if item['category'] == 'SKY':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['sky3'] = item['fcstValue']
            # 기온
        if item['category'] == 'TMN':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '0600':
                    weather_data3['tmn3'] = item['fcstValue']
        # 최고 기온
        if item['category'] == 'TMX':
            if item['fcstDate'] == dayafter:
                if item['fcstTime'] == '1500':
                    weather_data3['tmx3'] = item['fcstValue']

    return render(request, 'jeju.html', {'min7': weather_data['min7'], 'min4': weather_data['min4'],
                                           'min5': weather_data['min5'],
                                           'min6': weather_data['min6'],
                                           'max7': weather_data['max7'],
                                           'max4': weather_data['max4'], 'max5': weather_data['max5'],
                                           'max6': weather_data['max6'],
                                           'rnSt7Am': weather_data2['rnSt7Am'], 'rnSt4Am': weather_data2['rnSt4Am'],
                                           'rnSt5Am': weather_data2['rnSt5Am'],
                                           'rnSt6Am': weather_data2['rnSt6Am'],
                                           'wf7Am': weather_data2['wf7Am'],
                                           'wf4Am': weather_data2['wf4Am'], 'wf5Am': weather_data2['wf5Am'],
                                           'wf6Am': weather_data2['wf6Am'],
                                           'pop1': weather_data3['pop1'], 'sky1': weather_data3['sky1'],
                                           'pop2': weather_data3['pop2'], 'sky2': weather_data3['sky2'],
                                           'tmx1': weather_data3['tmx1'], 'tmx2': weather_data3['tmx2'],
                                           'tmn1': weather_data3['tmn1'], 'tmn2': weather_data3['tmn2'],
                                           'pop3': weather_data3['pop3'], 'sky3': weather_data3['sky3'],
                                           'tmx3': weather_data3['tmx3'], 'tmn3': weather_data3['tmn3']


                                           })



