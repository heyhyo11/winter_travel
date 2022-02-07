from unicodedata import category
from django.shortcuts import redirect, render
from .models import user_view
from API.models import db_insert
import random
from django.contrib.auth.decorators import login_required
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def main(request):
    data = db_insert.objects.all()
    data_dict = []
    for i in range(10):
        rand = random.randrange(len(data))
        d = data[rand]
        data_dict.append(d)
    return render(
        request,
        'main/index.html',
        {'datas':data_dict}
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
            user_check.save()

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

    print(similar_user_views)

    return redirect('/')
