from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>', views.detail, views.recommand, name='detail'),
    path('map/', views.thismap, name='maps'),
    path('test/', views.pictures, name='pictures'),
    path('d_p/<int:id>', views.detail_view, name='view'),
]