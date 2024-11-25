from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_category_detail'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brand_detail'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    # path('favorite', views.ProductFavorite.as_view(), name='product_favorite'),
]