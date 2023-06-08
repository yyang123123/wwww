from django.shortcuts import render
from datetime import date, datetime, timedelta
from urllib.parse import urlencode, quote_plus, unquote
import openai
import requests
from googletrans import Translator
from.models import Post

# Create your views here.
openai.api_key = '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'

date1 = datetime.today().strftime("%m월%d일")
today = datetime.today().strftime("%Y%m%d")

url3 = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
key = '8vmL%2FmpOsG19eWY%2Bbvi609ZBBMV%2FJ65TfFSy2M80l28%2BY5lDEy0Rm3fbglBrJEl51wWmC8s3RMetgEjgG0DKgw%3D%3D'


serviceKeyDecoded = unquote(key, 'UTF-8')
queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): 60, quote_plus('ny'): 127,
                                    quote_plus('dataType'): 'json', quote_plus('numOfRows'): '1000'})
res3 = requests.get(url3 + queryParams3, verify=False)
items3 = res3.json().get('response').get('body').get('items')

data3 = dict()
data3['date'] = today
weather_data3 = dict()

for item in items3['item']:
    if item['category'] == 'SKY':
        if item['fcstDate'] == today:
            if item['fcstTime'] == '0600':
                weather_data3['sky1'] = item['fcstValue']

if weather_data3['sky1'] == '1':
    word1 = '하늘이 맑은데'
elif weather_data3['sky1'] == '3':
    word1 = '하늘에 구름많은데'
elif weather_data3['sky1'] == '4':
    word1 = '하늘이 흐린데'


def gyeong(request):
    string_list = [date1, word1, '동대문디자인플라자'+'에','입고 갈 옷차림 추천해줘 설명없이']
    sentence = ''.join(string_list)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": sentence},
        ]
    )
    output_text = response["choices"][0]["message"]["content"]
    translator = Translator()
    content ='2006년 서울특별시청이 계획한 동대문디자인플라자(DDP)는 2014년 3월 21일 문을 열었다. DDP의 목적은 혁신과 개발의 위해 디자인적 사고를 이용하는 것이다. 또한 세계의 디자인 경향과, 21세기 창조적 지식 탄생지로서의 디자인 혁신을 소개하고 있다.'
    result = translator.translate(content).text
    content2='10:00 ~ 20:00 (공간별 운영시간 상이, 홈페이지 참조)'
    content3='연중무휴'
    content4='04566 서울 중구 을지로 281 (을지로7가, 디자인장터)'
    content5='2, 4, 5호선 동대문 역사 문화공원역 1, 10번 출구'
    result2 = translator.translate(content2).text
    result3 = translator.translate(content3).text
    result4 = translator.translate(content4).text
    result5 = translator.translate(content5).text
    chat = translator.translate(output_text).text
    region = '동대문디자인플라자'
    title = translator.translate(region).text
    return render(request, 'Dongdaemun.html', {'result': result, 'result2': result2, 'result3': result3,
                                           'result4': result4, 'result5': result5, 'content':content,'content2':content2,'content3':content3,'content4':content4,'content5':content5,
                                            'output_text': output_text, 'chat': chat, 'title':title, 'region': region})


