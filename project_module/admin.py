from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {
        'slug':('title',)
    }
    list_filter = ('is_active','is_delete')
    list_display = ('title','price','is_active','is_delete')
    list_editable = ('price','is_active')
    
admin.site.register(product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductTags)
admin.site.register(ProductBrand)
admin.site.register(Banners)
admin.site.register(ProductGallery)