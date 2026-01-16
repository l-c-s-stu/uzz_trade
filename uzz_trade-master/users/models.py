from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    phone = models.CharField(max_length=11, blank=True,null=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=True)
    student_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="学号")
    college = models.CharField(max_length=50, null=True, blank=True, verbose_name="学院")

    def __str__(self):
        return self.username