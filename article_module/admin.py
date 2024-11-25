from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from . import models
# Register your models here.


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title','url_title','parent','is_active']
    list_editable = ['url_title','parent','is_active']

class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user','created_date','parent']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','slug','is_active','author','created_date']
    list_editable = ['slug','is_active']
    
    def save_model(self, request: HttpRequest, obj: models.Article, form: Any, change: Any):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(models.ArticleCategory,ArticleCategoryAdmin)
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.ArticleComment,ArticleCommentAdmin)