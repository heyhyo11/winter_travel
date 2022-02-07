from unittest.util import _MAX_LENGTH
from django.db import models
from user.models import UserModel
from django_mysql.models import ListCharField

# Create your models here.

# class user_view(models.Model):
#     class Meta:
#         db_table = 'user_view'    
#     category = ListCharField(
#         base_field = models.CharField(max_length=10),
#         size=6,
#         max_length=(6*11),
#     )
#     category_count = ListCharField(
#         base_field = models.CharField(max_length=10),
#         size=6,
#         max_length=(6*11),
#     )
#     user_view = ListCharField(
#         base_field = models.CharField(max_length=10),
#         size=6,
#         max_length=(6*11),
#     )
#     name = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)

class user_view(models.Model):
    class Meta:
        db_table = 'user_view'
    category = models.TextField(max_length=500)
    category_count = models.TextField(max_length=500)
    user_view = models.TextField(max_length=5000)
    name = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)
