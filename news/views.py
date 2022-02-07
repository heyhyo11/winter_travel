from django.http import HttpResponse
from django.shortcuts import redirect, render
# from .models import Img
import datetime
from uuid import uuid4

# Create your views here.
def new(request):
    if request.method == 'POST':
        img_file = request.FILES['file']
        today = (datetime.datetime.now()).strftime("%Y%m%d")
        img_url = f'https://winterproject.s3.ap-northeast-2.amazonaws.com/uploads/{today}/{img_file}'
        Img.objects.create(Img=img_file, Img_url=img_url)
        return render(request,'news/result.html', {'img':img_url})
    return render(request, 'news/index.html')

