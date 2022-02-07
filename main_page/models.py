from django.db import models
from user.models import UserModel
from API.models import db_insert



class user_view(models.Model):
    class Meta:
        db_table = 'user_view'
    category = models.TextField(max_length=500)
    category_count = models.TextField(max_length=500)
    user_view = models.TextField(max_length=5000)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)


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

