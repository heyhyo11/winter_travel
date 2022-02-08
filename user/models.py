from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
<<<<<<< HEAD
        db_table = "user"
=======
        db_table = "USER"
>>>>>>> a7cc9a5b41863820fa0deb8a30070982954babfc
