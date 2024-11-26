from typing import Any
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from .models import Banners, product,ProductCategory,ProductBrand,ProductGallery
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Count
from utils.convertors import list_group
from utils.get_ip import get_ip
from project_module.models import VisitedProduct
# Create your views here.


class ProductListView(ListView):
    model = product
    template_name = 'project_module/project_module_list.html'
    context_object_name = 'product'
    ordering = ['price']
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        request : HttpRequest = self.request
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        query:product = product.objects.all()
        Product = query.order_by('-price').first()
        db_max_price = Product.price if Product is not None else 0
        context['min_price'] = min_price or 0
        context['max_price'] = max_price or db_max_price
        context['db_max_price'] = db_max_price
        context['banners'] = Banners.objects.filter(is_active=True,position = 'product_list')
        return context
    
    def get_queryset(self):
        query = super().get_queryset()
        cate = self.kwargs.get('cat')
        brand = self.kwargs.get('brand')
        q = self.request.GET.get('q')
        request : HttpRequest = self.request
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if q is not None:
            query = product.objects.search(q)
        if min_price is not None:
            query = query.filter(price__gte=min_price)
        if max_price is not None:
            query = query.filter(price__lte=max_price)
        if cate:
            query = query.filter(category__title_url__iexact=cate)
        elif brand:
            query = query.filter(brand__id__iexact=brand)
        return query.filter(is_active=True)


class ProductDetailView(DetailView):
    template_name = 'project_module/product_detail.html'
    model = product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        list__group =list(ProductGallery.objects.filter(products_id = self.object.id).all())
        list__group.insert(0,self.object)
        context['list_groups'] = list_group(list__group,3)
        brand_group = list(product.objects.filter(brand_id = self.object.brand_id)[:12])
        context["brand_groups"] = list_group(brand_group,3)
        user_ip = get_ip(self.request)
        user_id = self.request.user.id
        product_id = self.object.id
        visit = VisitedProduct.objects.filter(user_ip=user_ip,product_id_id=product_id).exists()
        if not visit:
            new_visit = VisitedProduct(user_ip= user_ip,user_id_id=user_id,product_id_id=product_id)
            new_visit.save()
        return context


def product_categories(request):
    product_cate = ProductCategory.objects.filter(is_active=True,is_delete=False)
    context = {'product_cate':product_cate}
    return render(request,'project_module/components/categories_components.html',context)


def product_brands(request):
    products_brand = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {'brands':products_brand}
    return render(request,'project_module/components/brands_components.html',context)