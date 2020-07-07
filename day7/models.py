from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phnoe = models.CharField(max_length=10,unique= True)
    class Meta:
        db_table = "day7_user"
        verbose_name="用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Computer(models.Model):
    name = models.CharField(max_length=20,unique=True)
    price = models.DecimalField(max_length=8,decimal_places=2,max_digits=10)
    brand = models.CharField(max_length=15,verbose_name='品牌')

    class Meta:
        db_table = "day7_computer"
        verbose_name="电脑"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
