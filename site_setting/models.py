from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='عنوان سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='ادرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت')
    about_us = models.TextField(verbose_name='متن درباره ما')
    site_logo = models.ImageField(upload_to='images/site-setting/',verbose_name='لوگوی سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'
    
    def __str__(self):
        return self.site_name
    
class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200,verbose_name='عنوان')
    
    class Meta:
        verbose_name = 'دسته یندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'
    
    def __str__(self):
        return self.title
    

class FooterLink(models.Model):
    title = models.CharField(max_length=200,verbose_name='عنوان')
    url = models.URLField(max_length=500,verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, verbose_name="دسته بندی", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'لینک  فوتر'
        verbose_name_plural = 'لینک های فوتر'
    
    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200,verbose_name='عنوان')
    url = models.URLField(max_length=500,verbose_name='لینک')
    url_title = models.CharField(max_length=200,verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/slider/',verbose_name='تصویر')
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'
    
    def __str__(self):
        return self.title