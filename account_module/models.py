from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(verbose_name='تصویر',null=True, blank=True)
    email_verification = models.CharField(verbose_name='تایید ایمیل', max_length=100)
    about_user = models.TextField(verbose_name='درباره ی کاربر',null=True, blank=True)
    address = models.TextField(verbose_name='ادرس',null=True, blank=True)
    
    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = ' اکانت ها'
        
    def __str__(self):
        return self.email
