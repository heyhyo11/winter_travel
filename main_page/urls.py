from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('view/<int:id>', views.user_view_in),
]
