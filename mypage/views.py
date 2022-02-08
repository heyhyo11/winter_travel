from django.shortcuts import render
from API.models import user_view, db_insert
from allauth.account.decorators import login_required

@login_required
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

    record = []

    for n in my_views[::-1]:
        user_history = db_insert.objects.get(id=n)
        record.append((user_history.img, user_history.title, user_history.address, user_history.id))

        if len(record) > 50:
            break

    return render(request, 'mypage/mypage.html', {'recommend': user_recommend, 'record': record})

