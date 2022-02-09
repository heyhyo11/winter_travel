from django.urls import path
from . import views

urlpatterns = [
    # path('data_insert', views.data_insert, name='data_insert'),
    path('view/<int:id>', views.user_view_in),
    path('delete/<int:id>', views.user_view_delete),
]
