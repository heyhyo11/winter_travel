from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.home, name='home'),

]
