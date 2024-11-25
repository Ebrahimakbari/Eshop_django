from django.db import models
from account_module.models import User

# Create your models here.


class ArticleCategory(models.Model):
    parent = models.ForeignKey(to='ArticleCategory', blank=True, null=True, verbose_name='والد', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    short_description = models.TextField(verbose_name='توضیح کوتاه')
    text = models.TextField(verbose_name='توضیح اصلی')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True,verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/article/', verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    article_category = models.ManyToManyField(to=ArticleCategory, verbose_name='دسته بندی ها')
    author = models.ForeignKey(User, verbose_name='نویسنده', on_delete=models.CASCADE, null=True,editable=False)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت',editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, verbose_name='عنوان مقاله', on_delete=models.CASCADE)
    parent = models.ForeignKey('ArticleComment', verbose_name="والد",null=True,blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name="متن نظر")

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'

    def __str__(self):
        return str(self.user)