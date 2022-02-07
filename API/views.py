from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import db_insert
import json




headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    } 
url = 'https://kr.trip.com/travel-guide/south-korea-100042/'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# max_location = int(soup.select('#__next > div:nth-child(2) > div > div.jsx-808517774.pagination-container.tc > div > ul > li ')[-1].text)
max_location = 3

# 지역구하기

def location(max_location):
    location = []
    location_code = []
    for i in range(2, max_location+1):
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
    category = [f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1003/",     # 건축 & 랜드마크
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1005/",         # 전시관
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1000/",         # 공원
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1002/",         # 유적지
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-169/",          # 자연
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1017/",         # 라이프스타일
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-77/",           # 종교 성지
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1004/",         # 전통/민속 체험
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-27/",           # 관광 투어
            f"https://kr.trip.com/travel-guide/city-{code}/tourist-attractions/type-1016/",]        # 스포츠
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
category = ['랜드마크','전시관','공원','유적지','자연','라이프스타일','성지','전통','관광투어','스포츠']

def area_data(location_info):
    
    for i in range(len(location_info)):
        print(f'{location_info[i][0]}href 주소 입력중...')
        
        category_href = category_list(location_info[i][1])
        for j in range(len(category)):
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

    title = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['poiName']
    db_serach = db_insert.objects.filter(title=title)
    if db_serach:
        return 
    try:
        tags = json.loads(script)['props']['pageProps']['appData']['overviewData']['basicInfo']['tagList']     
    except KeyError:
        tags = []

    img = json.loads(script)['props']['pageProps']['appData']['overviewData']['imageInfo']['imageList'][:4]
    
        
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