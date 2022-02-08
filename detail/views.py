import datetime
import json
from urllib import response
import folium
import pandas as pd
import requests
from django.shortcuts import render
from django.template.defaulttags import register
from .models import db_insert
from .models import db_recommend
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def detail_view(request):
    
    return render(request, 'detail\detail_main.html')


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
        for tag in taglist:
            print(tag)
        
        print(tag)
        print(taglist)
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
        print(X_int)
        print(Y_int)

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
        # f'{X_int}'
        # f'{Y_int}'


        # 값 요청
        res = requests.get(url, params=params)
        target = json.loads(res.content.decode('utf-8'))

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

        weather_data = pd.DataFrame({
            '카테고리': category,
            '예보 날짜': fcstDate,
            '예보 시간': fcstTime,
            '날씨 값': fcstValue,
        })


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

        weather_dic = {}
        for i in range(len(fcstDate_date)):
            weather_dic[i]= {
                'fcstDate_date': fcstDate_date[i],
                'fcstTime_hour': fcstTime_hour[i],
                'TMP_fcstValue': TMP_fcstValue[i],
                'POP_fcstValue': POP_fcstValue[i],
                'SKY_fcstValue': SKY_fcstValue[i],
            }
        
        # print(weather_dic.keys())
        # print(type(weather_dic))
        # print(type(fcstDate_date))
        return render(request, 'detail\detail_main.html', {'weather': weather_dic, 'result': result})


def thismap(request):
    location_x = 33.249958
    location_y = 126.413419
    location = {
        'x':location_x,
        'y':location_y
        }
    # location에 위치정보 받아오기
    # m = folium.Map(location=[location_x, location_y], zoom_start=15)
    # folium.Marker(
    #     # popup에 위치 이름값 받아서 지정해주기
    #     location=[location_x, location_y], popup='해운대', icon=folium.Icon(color="red", icon='star')).add_to(m)
    # m.save('detail/detail_sub/map.html')

    return render(request, 'detail/detail_sub/map.html', location)


def pictures(request):
    return render(request, 'detail/test.html')


def recommand(user):
    user_id = user
    user_views = db_recommend.objects.all()
    df = None
    for i in user_views:
        category = re.sub('[^가-핳,]', '', i.category)
        category_count = re.sub('[^0-9,]', '', i.category_count)
        category = category.split(',')
        category_count = category_count.split(',')
        userid = i.user_id
        for j in range(len(category)):
            df_temp = pd.DataFrame({
                'category': category[j],
                'count': category_count[j],
                'userid': userid
            }, index=[0])
            if df is not None:
                df = pd.concat([df, df_temp])
            else:
                df = df_temp

    # user별로 지역에 부여한 count 값을 볼 수 있도록 pivot table 사용
    title_user = df.pivot_table('count', index='category', columns='userid')

    # NaN 값은 그냥 0이라고 부여
    title_user = title_user.fillna(0)

    # 유저 1~610 번과 유저 1~610 번 간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(title_user, title_user)

    # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index,
                                     columns=title_user.index)

    print(user_based_collab)

    similar_user = user_based_collab[user_id.id].sort_values(ascending=False)[:2].index[1].tolist()

    similar_user_views = db_recommend.objects.get(user_id=similar_user).user_view.split(',')
    result = []
    if len(similar_user_views) > 5:
        for i in range(5):
            img = db_insert.objects.get(id=int(similar_user_views[i])).img
            img = (img, similar_user_views[i])
            result.append(img)
    else:
        for i in range(len(similar_user_views)):
            img = db_insert.objects.get(id=int(similar_user_views[i])).img
            img = (img, similar_user_views[i])
            result.append(img)

    return result