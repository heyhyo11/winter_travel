from django.shortcuts import render
from .models import user_view


def main(request):
    return render(
        request,
        'main/index.html'
    )

# def user_view(request):
#     location_list = ['서울', '제주', '서귀포', '부산', '대구', '강릉시', '청주', 
#                     '인천', '여수', '속초', '광주', '경주', '평창군', '양양', '수원', 
#                     '울산', '군산', '전주', '고성군', '거제시', '통영', '정선군', 
#                     '포항', '대전', '화성', '춘천', '홍천군', '가평군', '이천', 
#                     '삼척시', '천안', '안산', '진주', '고양', '창원', '보령시', 
#                     '용인', '양평', '원주시', '파주', '동해시', '목포', '아산시', 
#                     '충주', '부천', '남원시', '단양군', '안동시', '김해시', '예산군', 
#                     '남양주', '양산시', '무안', '횡성군', '부여군', '구리', '인제군', 
#                     '나주시', '태백시', '보은군', '제주도', '의왕', '연기군']
#     category_list = ['랜드마크','전시관','공원','유적지','자연','라이프스타일','성지','전통','관광투어','스포츠']

#     db = user_view.objects.filter(user=user)
#     for i in db.user_view:
        


#     return render(
#         request,
#         '.html'
#     )