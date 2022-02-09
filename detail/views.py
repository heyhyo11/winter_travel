import datetime
import json
from urllib import response
import folium
import pandas as pd
import requests
from django.shortcuts import render
from django.template.defaulttags import register
from API.models import db_insert
import pandas as pd


def detail(request, id):
    item = db_insert.objects.get(id=id)

    title = item.title
    x_address = item.x_address
    y_address = item.y_address
    content = item.content
    address = item.address
    img = item.img
    taglist = item.tag
    content = item.content

    result = {
        'title' : title,
        'x_address': x_address,
        'y_address': y_address,
        'content' : content,
        'address' : address,
        'img': img,
        'taglist' : taglist,
        'content': content,
    }

    now = datetime.datetime.now()

    base_time = now.strftime('%H'+"00")
    base_date = now.strftime("%Y%m%d")

    if 200<=int(base_time)<=400:
        base_hour = "0200"
    elif 500<=int(base_time)<=700:
        base_hour = "0500"
    elif 800<=int(base_time)<=1000:
        base_hour = "0800"
    elif 1100<=int(base_time)<=1300:
        base_hour = "1100"
    elif 1400<=int(base_time)<=1600:
        base_hour = "1400"
    elif 1700<=int(base_time)<=1900:
        base_hour = "1700"
    elif 2000<=int(base_time)<=2200:
        base_hour = "2000"
    elif int(base_time) == 2300:
        base_hour = "2300"
    else:
        base_hour = "2300"
        base_date = (now - datetime.timedelta(days=1)).strftime("%Y%m%d")

    X_int = int(float(x_address))
    Y_int = int(float(y_address))

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    params = {
        'serviceKey': 'xTnBP9tXQXWESKYWyRC9r6UfFnTmqn4CXeGOq3uyJornz5bqAVaQ0zy47BxH+8HycbQ0bT8XlKtv5tq9h+iQ0g==',
        'pageNo':'1',
        'numOfRows':"900",
        'dataType':'JSON',
        'base_date':{base_date},
        'base_time':{base_hour},
        'nx': f'{X_int}',
        'ny': f'{Y_int}',
    }

    # 값 요청
    res = requests.get(url, params=params)
    target = json.loads(res.content.decode('utf-8'))

    category = []
    fcstDate = []
    fcstTime = []
    fcstValue = []

    cate = target['response']['body']['items']['item']

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

    weather_data = pd.DataFrame({
        '카테고리': category,
        '예보 날짜': fcstDate,
        '예보 시간': fcstTime,
        '날씨 값': fcstValue,
    })


    weather_list = weather_data[(weather_data['카테고리'] == "TMP") | (weather_data['카테고리'] == "POP") | (weather_data['카테고리'] == "SKY")]


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


    # 예보날짜값
    # 날짜값 = split_date
    for date in fcstDate_f:
        split_date = date[6:8]
        fcstDate_date.append(split_date)




    #기온 예보값
    # 날씨값 = temperature
    for temperature in fcstValue_TMP:
        TMP_fcstValue.append(temperature)


    for hour in fcstTime_f:
        split_hour = hour[0:2]
        fcstTime_hour.append(split_hour)


    #강수확률 예보값
    #강수확률 = precipitation
    for precipitation in fcstValue_POP:
        POP_fcstValue.append(precipitation)

    for Sky in fcstValue_SKY:
        SKY_fcstValue.append(Sky)

    weather_dic = {}
    for i in range(len(fcstDate_date)):
        weather_dic[i]= {
            'fcstDate_date': fcstDate_date[i],
            'fcstTime_hour': fcstTime_hour[i],
            'TMP_fcstValue': TMP_fcstValue[i],
            'POP_fcstValue': POP_fcstValue[i],
            'SKY_fcstValue': SKY_fcstValue[i],
        }

    kind = db_insert.objects.get(id=id).category
    detail_category = db_insert.objects.order_by("?").filter(category=kind)[:5:]


    return render(request, 'detail/detail_main.html', {'weather': weather_dic, 'result': result, 'recommend_category':detail_category})

