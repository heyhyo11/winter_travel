from django.shortcuts import redirect, render
from API.models import top100_view, hot_view
from API.views import recommand
from allauth.account.decorators import login_required



def main(request):
    user = request.user
    user_login_check = request.user.is_authenticated
    top100 = top100_view.objects.all().order_by('-view_count')
    
    hot = hot_view.objects.all().order_by('-hot_count')
    if len(hot) < 5:
        hot = top100[:5]
    if user_login_check:
        recommand_user = recommand(user)
    else:
        recommand_user = []
    return render(
        request,
        'main/index.html',
        {'top100':top100,'recommand':recommand_user, 'hot':hot}
    )

