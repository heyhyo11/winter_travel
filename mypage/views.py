from django.shortcuts import render, redirect


def mypage(request):
    return render(request, 'mypage/mypage.html')
