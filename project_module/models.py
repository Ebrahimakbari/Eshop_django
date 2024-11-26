from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User

# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=300,verbose_name='عنوان دسته بندی',default='',db_index=True)
    title_url = models.CharField(max_length=300,verbose_name='عنوان دسته بندی لاتین',default='',db_index=True)
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    is_delete = models.BooleanField(default=False,verbose_name='حذف شده/نشده')

    def __str__(self):
        return f'{self.title}-{self.title_url}'
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

class ProductTags(models.Model):
    caption = models.CharField(max_length=300,verbose_name='کپشن-تگ')
    product_tag = models.ForeignKey("product", verbose_name=("تگ محصول"), on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        
class ProductBrand(models.Model):
    title = models.CharField(max_length=300,verbose_name='برند',db_index=True)
    is_active = models.BooleanField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند'
        
    
class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()
    
    def search(self,q):
        return self.get_queryset().filter(title__icontains=q)


class product(models.Model):
    title = models.CharField(max_length=300,verbose_name='عنوان محصول')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='images/product',verbose_name='تصویر محصول',null=True,blank=True)
    brand = models.ForeignKey("ProductBrand", verbose_name=("برند"), on_delete=models.CASCADE,null=True,blank=True)
    category = models.ManyToManyField("ProductCategory", verbose_name='دسته بندی')
    short_description = models.CharField(max_length=400,default=None,verbose_name='توضیحات کوتاه',db_index=True)
    description = models.TextField(max_length=500,default=None,verbose_name='توضیحات')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    is_delete = models.BooleanField(default=False,verbose_name='حذف شده/نشده')
    slug = models.SlugField(default='',null=False,blank=True,max_length=300,unique=True)
    
    
    objects = ProductManager()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    def save(self,*args, **kwargs):
        # self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    

class Banners(models.Model):
    class Position(models.TextChoices):
        product_list = 'product_list', 'لیست محصولات'
        home = 'home', 'صفحه اصلی'
    
    title = models.CharField(max_length=200,verbose_name='عنوان بنر')
    url = models.URLField(max_length=200,verbose_name='لینک بنر')
    image = models.ImageField(upload_to='images/banner', verbose_name='تصویر بنر')
    position = models.CharField(max_length=200,choices=Position.choices,verbose_name='موقعیت بنر')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'
        
class VisitedProduct(models.Model):
    user_ip = models.CharField(max_length=30,verbose_name='آیپی کاربر')
    product_id = models.ForeignKey(product, verbose_name='محصول', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,blank=True,null=True, verbose_name="کاربر id", on_delete=models.CASCADE)
    visited_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ بازدید')
    
    def __str__(self) -> str:
        return self.user_id.username
    
    class Meta:
        verbose_name = 'محصول بازدید شده'
        verbose_name_plural = 'محصولات بازدید شده'
        
class ProductGallery(models.Model):
    products = models.ForeignKey(product, verbose_name="محصول", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/gallery', verbose_name='تصویر محصول')

    def __str__(self) -> str:
        return self.products.title
    
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural ="تصاویر محصول"