from django.db import models

class Img(models.Model):
    class Meta:
        db_table ='img'
    Img = models.FileField(upload_to='uploads/%Y%m%d')
    Img_url = models.CharField(max_length=250)
