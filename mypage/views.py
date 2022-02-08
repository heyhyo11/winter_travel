from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import user_view



def mypage(request):
    user_id = request.user

    user_category = user_view.objects.get(user_id=user_id.id).category.split(',')
    user_recommend = []
    views = user_view.objects.get(user_id=user_id.id).user_view.split(',')
    my_views = []

    for i in user_category:
        user_recommend.append(i)

    for j in views:
        my_views.append(j)


    return render(request, 'mypage/mypage.html', {'recommend': user_recommend})

