from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
import site_setting
import site_setting.models
from site_setting.models import Slider
from utils.convertors import list_group
from utils.get_ip import get_ip
from project_module.models import ProductCategory, product,VisitedProduct
from django.db.models import Count,Sum

# Create your views here.

class HomeIndexView(TemplateView):
    template_name='home_module/home_index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active = True)
        list__group = product.objects.filter(is_active = True,is_delete = False).order_by('-id')[:12]
        context['list_groups'] = list_group(list__group,4)
        visited = product.objects.filter(is_active = True,is_delete = False).annotate(count=Count('visitedproduct')).order_by('-count')[:12]
        context['visited_groups'] = list_group(visited,4)
        categories = list(ProductCategory.objects.annotate(category_count=Count('product')).filter(is_active = True,is_delete = False,category_count__gt = 0)[:6])
        category_list = []
        for category in categories:
            my_dict = {
                'id' : category.id,
                'title': category.title,
                'product':list(category.product_set.all())
            }
            category_list.append(my_dict)
        context['categories'] = category_list
        orders =product.objects.filter(orderdetail__order__is_paid=True).annotate(p_count = Sum('orderdetail__count')).order_by('p_count')
        context['most_sailed'] = list_group(orders,4)
        return context


def footer_component(request):
    setting = site_setting.models.SiteSetting.objects.filter(is_main_setting = True).first()
    footer_link = site_setting.models.FooterLinkBox.objects.all()
    context = {
        "footer_link_boxes":footer_link,
        'site_setting':setting
    }
    return render(request, 'shared/footer_component.html',context)


def header_component(request):
    setting = site_setting.models.SiteSetting.objects.filter(is_main_setting = True).first()
    context = {
        'site_setting':setting
    }
    return render(request, 'shared/header_component.html',context)


class AboutUs(TemplateView):
    template_name = 'home_module/about_page.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting = site_setting.models.SiteSetting.objects.filter(is_main_setting = True).first()
        context['site_setting'] = setting
        return context     