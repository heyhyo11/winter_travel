from django.db import models

# class Img(models.Model):
#     class Meta:
#         db_table ='img'
#     Img = models.FileField(upload_to='uploads/%Y%m%d')
#     Img_url = models.CharField(max_length=250)


class db_search(models.Model):
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
