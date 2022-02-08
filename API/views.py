from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from .models import db_insert, top100_view, hot_view, user_view
import json
import re
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

# ============================== view_list ===================

def user_view_in(request, id):
    user_id = request.user
    item_category= db_insert.objects.get(id=id)
    item_category = item_category.category
    try:
        user_check = user_view.objects.get(user_id=user_id.id)
    except:
        category = item_category
        category_count = '1'
        view_list = str(id)

        user_view.objects.create(
            user_id = user_id.id,
            category = category,
            category_count = category_count,
            user_view = view_list,
            last_view_category = item_category
        )
    else:
        category = re.sub('[^가-핳,]','',user_check.category)
        category_count = re.sub('[^0-9,]','',user_check.category_count)
        user_view_list = re.sub('[^0-9,]','',user_check.user_view)

        category = category.split(',')
        category_count = category_count.split(',')
        user_view_list = user_view_list.split(',')


        if str(id) not in user_view_list:
            user_view_list.append(str(id))
            if item_category in category:
                index = category.index(item_category)
                category_count[index]= str(int(category_count[index])+1)
            else:
                category.append(item_category)
                category_count.append('1')

            user_check.category = ','.join(category)
            user_check.category_count = ','.join(category_count)
            user_check.user_view = ','.join(user_view_list)
            user_check.last_view_category = item_category
            user_check.save()

    try:
        view_count = top100_view.objects.get(item_id=id)
    except:
        view_count = top100_view.objects.create(
            item_id = id,
            view_count = 1
        )
    else:
        count = view_count.view_count + 1
        view_count.view_count = count
        view_count.save()

    try:
        view_count = hot_view.objects.get(item_id=id)
    except:
        view_count = hot_view.objects.create(
            item_id = id,
            hot_count = 1
        )
    else:
        count = view_count.hot_count + 1
        view_count.hot_count = count
        view_count.save()

    return redirect('/')


# ============================ 추천 시스템 ======================

def recommand(user):
    user_id = user
    result = []
    num = []
    id = []
    try:
        user_in_view = user_view.objects.get(user_id=user_id.id)
    except:
        num = []
        # 랜덤 5개
        items = db_insert.objects.all()
        for i in range(15):
            rand = random.randrange(0, len(items))
            while rand in num and str(items[rand].id) not in id:
                rand = random.randrange(0, len(items))
            img = (items[rand].img, items[rand].id)
            result.append(img)
            num.append(img)
            id.append(items[rand].id)
    else:
        user_views = user_view.objects.all()
        df = None
        for i in user_views:
            category = re.sub('[^가-핳,]','',i.category)
            category_count = re.sub('[^0-9,]','',i.category_count)
            category = category.split(',')
            category_count = category_count.split(',')
            userid = i.user_id
            for j in range(len(category)):
                df_temp = pd.DataFrame({
                'category':category[j],
                'count':category_count[j],
                'userid' : userid
                }, index = [0])
                if df is not None:
                    df = pd.concat([df, df_temp])
                else:
                    df = df_temp

        # user별로 지역에 부여한 count 값을 볼 수 있도록 pivot table 사용
        title_user = df.pivot_table('count', index='userid', columns='category')

        # NaN 값은 그냥 0이라고 부여
        title_user = title_user.fillna(0)

        # 유저 1~610 번과 유저 1~610 번 간의 코사인 유사도를 구함
        user_based_collab = cosine_similarity(title_user, title_user)

        # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
        user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index,
                                                columns=title_user.index)


        similar_user = user_based_collab[user_id.id].sort_values(ascending=False)[:2].index[1].tolist()

        similar_user_views = user_view.objects.get(user_id=similar_user).user_view.split(',')


        # 유사도 높은 유저 리스트 랜덤 5개
        if len(similar_user_views) > 5:
            for i in range(5):
                rand = random.randrange(0,len(similar_user_views))
                while rand in num:
                    rand = random.randrange(0,len(similar_user_views))
                img = db_insert.objects.get(id=int(similar_user_views[rand])).img
                img = (img,similar_user_views[rand])
                result.append(img)
                num.append(rand)
                id.append(similar_user_views[rand])
        else:
            for i in range(len(similar_user_views)):
                rand = random.randrange(0,len(similar_user_views))
                while rand in num:
                    rand = random.randrange(0,len(similar_user_views))
                img = db_insert.objects.get(id=int(similar_user_views[rand])).img
                img = (img,similar_user_views[rand])
                result.append(img)
                num.append(rand)
                id.append(similar_user_views[rand])

        num = []
        # 마지막 카테고리 5개
        last_category = user_view.objects.get(user_id=user_id.id).last_view_category
        rand_category = db_insert.objects.filter(category=last_category)
        for i in range(len(rand_category)):
            if i > 4:
                break
            else:
                rand = random.randrange(0, len(rand_category))
                while rand in num and str(rand_category[rand].id) not in id:
                    rand = random.randrange(0, len(rand_category))
                img = (rand_category[rand].img, rand_category[rand].id)
                result.append(img)
                num.append(img)
                id.append(rand_category[rand].id)
    
        num = []
        # 랜덤 5개
        items = db_insert.objects.all()
        for i in range(5):
            rand = random.randrange(0, len(items))
            while rand in num and str(items[rand].id) not in id:
                rand = random.randrange(0, len(items))
            img = (items[rand].img, items[rand].id)
            result.append(img)
            num.append(img)
            id.append(items[rand].id)

    return result

# ========================== 크롤링 =============================

# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
#     } 
# url = 'https://kr.trip.com/travel-guide/south-korea-100042/'
# page = requests.get(url, headers=headers)
# soup = BeautifulSoup(page.content, 'html.parser')
# # max_location = int(soup.select('#__next > div:nth-child(2) > div > div.jsx-808517774.pagination-container.tc > div > ul > li ')[-1].text)
# max_location = 1

# 지역구하기

def location(max_location):
    location = []
    location_code = []
    for i in range(1, max_location+1):
        url = f'https://kr.trip.com/travel-guide/south-korea-100042/{i}/'
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.select('#__next > div:nth-child(2) > div > div:nth-child(4) > div > div > div > p > a')
        for i in range(len(name)):
            location.append(name[i].text)
            location_code.append(name[i].get('href').split('/')[-2].split('-')[-1])

    return list(zip(location, location_code))
    

# 카테고리별 주소, 마지막페이지 구하기

def category_list(code):
    if code == '234':
        category = [f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1003/",     # 건축 & 랜드마크
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1005/",         # 전시관
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1000/",         # 공원
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1002/",         # 유적지
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-169/",          # 자연
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1017/",         # 라이프스타일
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-77/",           # 종교 성지
                f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-27/",           # 관광 투어
                    ]        
        category_length = []        
        for i in category:
            page = requests.get(i, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            # last_page = int(soup.select_one('#list > div.gl-poi-list_page > div > div > ul > li:nth-last-child(1) > a').text)
            last_page = soup.select('#list > div.gl-poi-list_page > div > div > ul > li > a')
            try:
                last_page = int(last_page[-1].text)
            except IndexError:
                print(last_page)
                print(i)
            category_length.append(last_page)

    return list(zip(category, category_length))


# 카테고리별 아이템 주소 구하기
def category_page_list(urls,length, location, category):
    try:
        for i in range(1,length+1):
            url = f"{urls}{i}.html"
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            page_item = soup.select('#list > div.gl-poi-list_list > div > a')
            for j in page_item:
                find_item(category,j.get('href'))
                print(category)
            print(f"{location} - {i} 번째 페이지 탐색중..")
    except TypeError:
        print(length)
    return  True


# 카테고리별 데이터 뽑기
category = ['랜드마크','전시관','공원','유적지','자연','라이프스타일','성지','관광투어',]

def area_data(location_info):
    
    for i in range(len(location_info)):
        print(f'{location_info[i][0]}href 주소 입력중...')
        
        category_href = category_list(location_info[i][1])

        for j in range(7,len(category)):
            category_page_list(category_href[j][0], category_href[j][1], location_info[i][0], category[j])
    return True



# def sub_latitude_longitude(address):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')        # Head-less 설정
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome('chromedriver', options=options)
#     print('위도 경도 변환')
#     url = 'https://www.google.co.kr/maps/place/'
#     driver.get(url)
#     input = driver.find_element(By.ID,'searchboxinput')
#     time.sleep(3)
#     input.send_keys(address)    
#     button = driver.find_element(By.ID,'searchbox-searchbutton')
#     button.click()
#     time.sleep(6)
#     result = driver.current_url.split('data')[0].split('@')[-1].split(',')
#     x = result[0]
#     y = result[1]
#     return x,y 

# geo_local = Nominatim(user_agent='South Korea')
# def latitude_longitude(address):
#     try:
#         geo = geo_local.geocode(address)
#         x = geo.latitude
#         y = geo.longitude
#     except AttributeError:
#         x,y = sub_latitude_longitude(address)
#     return x,y


def find_item(category,url):
    page = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        script = soup.find_all('script')[16].text
    except IndexError:
        return
    location = json.loads(script)['props']['pageProps']['appData']['overviewData']['districtInfo']['districtName']
    if location != '서울':
        return
    title = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['poiName']
    db_serach = db_insert.objects.filter(title=title)
    if db_serach:
        return 
    try:
        tags = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['tagList']     
    except KeyError:
        tags = []

    img = json.loads(script)['props']['pageProps']['appData']['overviewData']['imageInfo']['imageList']
    img = img[0]
        
    address = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['address']
#
    content = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['introduction']
    try:
        x = json.loads(script)['props']['pageProps']['appData']['overviewData']['districtInfo']['coordinate']['latitude']
    except KeyError:
        return
    y = json.loads(script)['props']['pageProps']['appData']['overviewData']['districtInfo']['coordinate']['longitude']
    # X = 위도, y = 경도
    
    db_insert.objects.create(
        location=location,
        category=category, 
        title=title,
        tag = tags,
        img = img,
        address = address,
        x_address = x,
        y_address = y,
        content = content
    )
    print('데이터 입력')
    return 

# Create your views here.

def data_insert(request):
    location_info = location(max_location)
    data = area_data(location_info)
    return render(request, 'news/result.html',{'msg':'hello'})