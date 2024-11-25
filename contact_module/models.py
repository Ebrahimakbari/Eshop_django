from django.db import models

# Create your models here.
class ContactUs(models.Model):
    title = models.CharField(max_length=300,verbose_name='عنوان')
    email = models.EmailField(max_length=300,verbose_name='ایمیل')
    full_name = models.CharField(max_length=300,verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='ایجاد شده در')
    response = models.TextField(verbose_name='پاسخ',blank=True,null=True)
    is_read_by_admin = models.BooleanField(default=False,verbose_name=' خوانده شده توسط مدیر ')
    
    class Meta:
        verbose_name = 'تماس'
        verbose_name_plural = 'تماس ها'
        
    def __str__(self):
        return self.title
    

class ProfileModel(models.Model):
    image = models.ImageField(upload_to='images',verbose_name='تصویر پروفایل')