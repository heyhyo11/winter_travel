from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import user_view


def mypage(request):

    user_views = user_view.objects.get(user_id = 1).category


    result = []

    for i in user_views:
        result.append(i)

    print(result)

    return render(request, 'mypage/mypage.html', {'recommend': result})
