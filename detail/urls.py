from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.detail, name='detail'),
    path('map/', views.thismap, name='maps'),
    path('weather/', views.weather, name='weater'),
]
