from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>', views.detail, name='detail'),
]