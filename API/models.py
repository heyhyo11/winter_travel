from django.db import models
from user.models import UserModel


# Create your models here.

class db_insert(models.Model):
    class Meta:
        db_table ='data_1'
    location = models.CharField(max_length=50, null=False)
    category = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=255, unique=True)
    tag = models.TextField(null=True)
    img = models.TextField(null=False)
    address = models.CharField(max_length=250)
    x_address = models.CharField(max_length=50)
    y_address = models.CharField(max_length=50)
    content = models.TextField(null=False, max_length=2500)


class user_view(models.Model):
    class Meta:
        db_table = 'user_view'
    category = models.TextField(max_length=500)
    category_count = models.TextField(max_length=500)
    user_view = models.TextField(max_length=5000)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)
    last_view_category = models.CharField(max_length=50)


class top100_view(models.Model):
    class Meta:
        db_table = 'top100'
    item = models.OneToOneField(db_insert, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)

class hot_view(models.Model):
    class Meta:
        db_table = 'hot'
    item = models.OneToOneField(db_insert, on_delete=models.CASCADE)
    hot_count = models.IntegerField(default=0)