from django.db import models
from user.models import UserModel


class db_insert(models.Model):
    class Meta:
        db_table = 'data_1'
    location = models.CharField(max_length=50, null=False)
    category = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=255, unique=True)
    tag = models.TextField(null=True)
    img = models.TextField(null=False)
    address = models.CharField(max_length=250)
    x_address = models.CharField(max_length=50)
    y_address = models.CharField(max_length=50)
    content = models.TextField(null=False, max_length=2500)


class db_recommend(models.Model):
    class Meta:
        db_table = 'user_view'
    category = models.TextField(max_length=500)
    category_count = models.TextField(max_length=500)
    user_view = models.TextField(max_length=5000)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)
    last_view_category = models.CharField(max_length=50)