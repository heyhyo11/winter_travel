from django.db import models
from user.models import UserModel

class db_recommend(models.Model):
    class Meta:
        db_table = 'user_view'
    category = models.TextField(max_length=500)
    category_count = models.TextField(max_length=500)
    user_view = models.TextField(max_length=5000)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True)
    last_view_category = models.CharField(max_length=50)