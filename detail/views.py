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
nx=1
ny=1

if Post.objects.get(pk=1): #경복궁
    nx = '51'
    ny = '32'

serviceKeyDecoded = unquote(key, 'UTF-8')
queryParams3 = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded,
                                    quote_plus('pageNo'): '1', quote_plus('base_date'): today,
                                    quote_plus('base_time'): '0200', quote_plus('nx'): nx, quote_plus('ny'): ny,
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
    posts = Post.objects.get(pk=1)
    string_list = [date1, word1, posts.region+'에','입고 갈 옷차림 추천해줘 설명없이']
    sentence = ''.join(string_list)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": sentence},
        ]
    )
    output_text = response["choices"][0]["message"]["content"]
    translator = Translator()
    result = translator.translate(posts.content).text
    result2 = translator.translate(posts.sub_content2).text
    result3 = translator.translate(posts.sub_content3).text
    result4 = translator.translate(posts.sub_content4).text
    result5 = translator.translate(posts.sub_content5).text
    result6 = translator.translate(posts.sub_content6).text
    chat = translator.translate(output_text).text
    title = translator.translate(posts.region).text
    return render(request, 'gyeong.html', {'result': result, 'result2': result2, 'result3': result3,
                                           'result4': result4, 'result5': result5, 'result6': result6,
                                           'posts': posts, 'output_text': output_text, 'chat': chat, 'title':title} )


def Namsan(request):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "2016년 롤드컵 우승팀은 어디야?"},
        ]
    )
    output_text = response["choices"][0]["message"]["content"]

    posts = Post.objects.get(pk=1)
    translator = Translator()
    result = translator.translate(posts.content).text
    result2 = translator.translate(posts.sub_content2).text
    result3 = translator.translate(posts.sub_content3).text
    result4 = translator.translate(posts.sub_content4).text
    result5 = translator.translate(posts.sub_content5).text
    result6 = translator.translate(posts.sub_content6).text
    chat = translator.translate(output_text).text
    title = translator.translate(posts.region).text
    return render(request, 'Namsan.html', {'result': result, 'result2': result2, 'result3': result3,
                                           'result4': result4, 'result5': result5, 'result6': result6,
                                           'posts': posts, 'output_text': output_text, 'chat': chat, 'title':title})

