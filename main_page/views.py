from unicodedata import category
from django.shortcuts import redirect, render
from .models import user_view, top100_view, hot_view
from API.models import db_insert
import random
from allauth.account.decorators import login_required
import re
import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity

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

        print(user_based_collab)

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

def main(request):
    user = request.user
    user_login_check = request.user.is_authenticated
    top100 = top100_view.objects.all().order_by('-view_count')
    hot = hot_view.objects.all().order_by('-hot_count')
    if user_login_check:
        recommand_user = recommand(user)
    else:
        recommand_user = []
    return render(
        request,
        'main/index.html',
        {'top100':top100,'recommand':recommand_user, 'hot':hot}
    )


@login_required
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
