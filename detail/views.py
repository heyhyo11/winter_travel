from django.shortcuts import render

# Create your views here.
# from bs4 import BeautifulSoup
import pandas as pd
import time
from django.shortcuts import render
import folium
import requests
import json
from pytz import timezone
from datetime import datetime
from django.template.defaulttags import register
# Create your views here.


def detail(request):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    now = datetime.now(timezone('Asia/Seoul'))
    print(now)
    # KST = timezone('Asial/Seoul')
    # now = datetime.datetime.now()
    # now = now.astimezone(KST)

    base_date = now.strftime("%Y%m%d")  # "20200214" == 기준 날짜
    base_time = now.strftime("%H"+"00")  # 날씨 값
    print(base_date)
    print(base_time)
    params = {
        'serviceKey': 'xTnBP9tXQXWESKYWyRC9r6UfFnTmqn4CXeGOq3uyJornz5bqAVaQ0zy47BxH%2B8HycbQ0bT8XlKtv5tq9h%2BiQ0g%3D%3D',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': {base_date},
        'base_time': '0500',
        'nx': '33',
        'ny': '126'
    }

    # 값 요청
    response = requests.get(url, params=params)
    print(type(response))
    print(response)
    # print(response.content)
    # content = response.text
    # print(type(content))
    target = json.loads(response.content.decode('utf-8'))
    # target = response.content
    # print(type(target))

    # print(target)
    # print(target['response']['body']['items']['item'])

    # print(response)

    category = []
    fcstDate = []
    fcstTime = []
    fcstValue = []

    cate = target['response']['body']['items']['item']

    # print(cate)
    # print(type(cate[0]['fcstDate']))

    for cate_list in cate:
        # print(cate_list)
        if cate_list['fcstTime'] == '0300':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0600':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0600':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0900':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1200':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1500':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1800':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '2100':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0000':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        else:
            continue

            # print(cate_list)

    weather_data = pd.DataFrame({
        '카테고리': category,
        '예보 날짜': fcstDate,
        '예보 시간': fcstTime,
        '날씨 값': fcstValue,
    })

    weather_data

    weather_list = weather_data[(weather_data['카테고리'] == "TMP") | (
        weather_data['카테고리'] == "POP") | (weather_data['카테고리'] == "SKY")]
    weather_list


    TMP_list = weather_list[weather_list['카테고리'] == 'TMP']
    POP_list = weather_list[weather_list['카테고리'] == 'POP']
    SKY_list = weather_list[weather_list['카테고리'] == 'SKY']


    fcstDate_f = TMP_list['예보 날짜']
    fcstTime_f = TMP_list['예보 시간']
    fcstValue_TMP = TMP_list['날씨 값']
    fcstValue_POP = POP_list['날씨 값']
    fcstValue_SKY = SKY_list['날씨 값']


    fcstDate_date = []
    fcstTime_hour = []
    TMP_fcstValue = []
    POP_fcstValue = []
    SKY_fcstValue = []
    # print(fcstTime_f)


    print('_________________________________')
    # 예보날짜값
    # 날짜값 = split_date
    for date in fcstDate_f:
        split_date = date[6:8]
        fcstDate_date.append(split_date)
        # print(date)

    # print(fcstDate_f)

    #기온 예보값
    # 날씨값 = temperature
    for temperature in fcstValue_TMP:
        TMP_fcstValue.append(temperature)
        # print(temperature)

    print('_________________________________')

    for hour in fcstTime_f:
        split_hour = hour[0:2]
        fcstTime_hour.append(split_hour)
        # print(split_hour)


    #강수확률 예보값
    #강수확률 = precipitation
    for precipitation in fcstValue_POP:
        POP_fcstValue.append(precipitation)
        # print(POP_fcstValue)

    for Sky in fcstValue_SKY:
        SKY_fcstValue.append(Sky)
        # print(SKY_fcstValue)


    # print(fcstTime_f)
    # print(type(fcstTime_f[0]))
    # print(len(fcstTime_f[0]))
    # split_date = TMP_fcstDate.substring(0, 2)
    # hour=[]
    # print(split_date)
    weather_dic = {}
    for i in range(len(fcstDate_date)):
        weather_dic[i]= {
            'fcstDate_date': fcstDate_date[i],
            'fcstTime_hour': fcstTime_hour[i],
            'TMP_fcstValue': TMP_fcstValue[i],
            'POP_fcstValue': POP_fcstValue[i],
            'SKY_fcstValue': SKY_fcstValue[i],
        }
    print(weather_dic.keys())
    # print(type(weather_dic))
    # print(type(fcstDate_date))
    return render(request, 'detail\detail_main.html', {'weather': weather_dic})


def thismap(request):

    # location에 위치정보 받아오기
    m = folium.Map(location=[35.167107, 129.167743], zoom_start=15)
    folium.Marker(
        # popup에 위치 이름값 받아서 지정해주기
        location=[35.167107, 129.167743], popup='해운대', icon=folium.Icon(color="red", icon='star')).add_to(m)
    m.save('myapp/templates/myapp/map.html')

    return render(request, 'detail\detail_sub\map.html')


def weather(request):

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    now = datetime.now(timezone('Asia/Seoul'))
    print(now)
    # KST = timezone('Asial/Seoul')
    # now = datetime.datetime.now()
    # now = now.astimezone(KST)

    base_date = now.strftime("%Y%m%d")  # "20200214" == 기준 날짜
    base_time = now.strftime('%H'+"00")  # 날씨 값
    # print(base_date)
    # print(base_time)
    params = {
        'serviceKey': 'xTnBP9tXQXWESKYWyRC9r6UfFnTmqn4CXeGOq3uyJornz5bqAVaQ0zy47BxH+8HycbQ0bT8XlKtv5tq9h+iQ0g==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': '20220206',
        'base_time': '0200',
        'nx': '33',
        'ny': '126'
    }

    # 값 요청
    response = requests.get(url, params=params)
    print(type(response))
    # print(response)
    # print(response.content)
    # content = response.text
    # print(type(content))
    target = json.loads(response.content.decode('utf-8'))
    # target = response.content
    # print(type(target))

    # print(target)
    # print(target['response']['body']['items']['item'])
    # print(response)

    category = []
    fcstDate = []
    fcstTime = []
    fcstValue = []

    cate = target['response']['body']['items']['item']
    # print(cate)
    # print(type(cate[0]['fcstDate']))

    for cate_list in cate:
        # print(cate_list)
        if cate_list['fcstTime'] == '0300':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0600':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0600':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0900':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1200':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1500':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '1800':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '2100':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        elif cate_list['fcstTime'] == '0000':
            fcstDate.append(cate_list['fcstDate'])
            fcstTime.append(cate_list['fcstTime'])
            category.append(cate_list['category'])
            fcstValue.append(cate_list['fcstValue'])
        else:
            continue

            # print(cate_list)

    weather_data = pd.DataFrame({
        '카테고리': category,
        '예보 날짜': fcstDate,
        '예보 시간': fcstTime,
        '날씨 값': fcstValue,
    })

    weather_data

    weather_list = weather_data[(weather_data['카테고리'] == "TMP") | (
        weather_data['카테고리'] == "POP") | (weather_data['카테고리'] == "SKY")]
    weather_list

    TMP_list = weather_list[weather_list['카테고리'] == 'TMP']
    POP_list = weather_list[weather_list['카테고리'] == 'POP']
    SKY_list = weather_list[weather_list['카테고리'] == 'SKY']

    fcstDate_f = TMP_list['예보 날짜']
    fcstTime_f = TMP_list['예보 시간']
    fcstValue_TMP = TMP_list['날씨 값']
    fcstValue_POP = POP_list['날씨 값']
    fcstValue_SKY = SKY_list['날씨 값']

    fcstDate_date = []
    fcstTime_hour = []
    TMP_fcstValue = []
    POP_fcstValue = []
    SKY_fcstValue = []
    # print(fcstTime_f)

    print('_________________________________')
    # 예보날짜값
    # 날짜값 = split_date
    for date in fcstDate_f:
        split_date = date[6:8]
        fcstDate_date.append(split_date)
        # print(date)

    # print(fcstDate_f)

    #기온 예보값
    # 날씨값 = temperature
    for temperature in fcstValue_TMP:
        TMP_fcstValue.append(temperature)
        # print(temperature)

    print('_________________________________')

    for hour in fcstTime_f:
        split_hour = hour[0:2]
        fcstTime_hour.append(split_hour)
        # print(split_hour)

    #강수확률 예보값
    #강수확률 = precipitation
    for precipitation in fcstValue_POP:
        POP_fcstValue.append(precipitation)
        # print(POP_fcstValue)

    for Sky in fcstValue_SKY:
        SKY_fcstValue.append(Sky)
        # print(SKY_fcstValue)

    # print(fcstTime_f)
    # print(type(fcstTime_f[0]))
    # print(len(fcstTime_f[0]))
    # split_date = TMP_fcstDate.substring(0, 2)
    # hour=[]
    # print(split_date)
    weather_dic = {}
    for i in range(len(fcstDate_date)):
        weather_dic[i] = {
            'fcstDate_date': fcstDate_date[i],
            'fcstTime_hour': fcstTime_hour[i],
            'TMP_fcstValue': TMP_fcstValue[i],
            'POP_fcstValue': POP_fcstValue[i],
            'SKY_fcstValue': SKY_fcstValue[i],
        }
    print(weather_dic.keys())
    # print(type(weather_dic))
    # print(type(fcstDate_date))
    return render(request, 'detail/detail_main.html', {'weather': weather_dic})


# @register.filter
# def get_range(value):

#     return range(len(value))
