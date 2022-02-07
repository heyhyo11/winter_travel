from unicodedata import category
from django.shortcuts import redirect, render
from .models import user_view
from API.models import db_insert
import random
from django.contrib.auth.decorators import login_required
import re





def main(request):
    data = db_insert.objects.all()
    data_dict = []
    for i in range(10):
        rand = random.randrange(len(data))
        d = data[rand]
        data_dict.append(d)
    print(data_dict)
    return render(
        request,
        'main/index.html',
        {'datas':data_dict}
    )

@login_required
def user_view_in(request, id):
    user = request.user
    item_category= db_insert.objects.get(id=id)
    item_category = item_category.category
    try:
        user_check = user_view.objects.get(name_id=user)
    except:
        category = item_category+','
        category_count = '1,'
        view_list = str(id) + ','
        user_view.objects.create(
            name_id = user,
            category = [category],
            category_count = [category_count],
            user_view = [view_list],
        )
    else:
        category = re.sub('[^가-핳,]','',user_check.category)
        category_count = re.sub('[^0-9,]','',user_check.category_count)
        user_view_list = re.sub('[^0-9,]','',user_check.user_view)

        category = category.split(',')
        category_count = category_count.split(',')
        user_view_list = user_view_list.split(',')
        print(item_category, category)
        if item_category in category:
            index = category.index(item_category)
            category_count[index]= int(category_count[index])+1
            if str(id) not in user_view_list:
                user_view_list.append(id)
            
        else:
            category.append(item_category)
            category_count.append('1')
            user_view_list.append(str(id))

            print(category)
            print(category_count)
            print(user_view_list)

            user_check.category = ','.join(category)
            user_check.category_count = ','.join(category_count)
            user_check.user_view = ','.join(user_view_list)
            user_check.save()
        
            
            
        # user_view.objects.update()
        
    
    
    return redirect('')