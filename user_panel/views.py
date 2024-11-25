from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from paymant_module.models import Order, OrderDetail
from .forms import EditProfileFormsModel, ChangePasswordForms
from account_module.models import User
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from paymant_module.models import Order
# Create your views here.

@method_decorator(login_required,name='dispatch')
class UserPanelDashboard(TemplateView):
    template_name = 'user_panel/user_panel.html'


@method_decorator(login_required,name='dispatch')
class EditProfileClass(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        user_form = EditProfileFormsModel(instance=current_user)
        context = {
            'form': user_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/edit_profile_panel.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        user_form = EditProfileFormsModel(
            request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save(commit=True)
        context = {
            'form': user_form,
            'current_user': current_user
        }
        return render(request, 'user_panel/edit_profile_panel.html', context)


@method_decorator(login_required,name='dispatch')
class ChangePasswordClass(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = ChangePasswordForms()
        context = {
            'form':form,
            'current_user': current_user
        }
        return render(request,'user_panel/change_password.html',context)
    def post(self,request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = ChangePasswordForms(request.POST)
        if form.is_valid():
            if current_user.check_password(form.cleaned_data['old_password']):
                current_user.set_password(form.cleaned_data['new_password'])
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('old_password','پسورد فعلی اشتباه است')
        context = {
            'form':form,
        }
        return render(request,'user_panel/change_password.html',context)


@method_decorator(login_required,name='dispatch')
class PaymentHistory(ListView):
    model = Order
    template_name = 'user_panel/payment_history.html'
    context_object_name = 'historys'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        queryset = queryset.filter(is_paid=True,user_id =self.request.user.id).first()
        return queryset


@method_decorator(login_required,name='dispatch')
class PaymentDetail(ListView):
    model = Order
    template_name = 'user_panel/payment_detail.html'
    context_object_name = 'current_order'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        queryset = queryset.filter(is_paid=True,user_id =self.request.user.id).first()
        return queryset


@login_required
def side_panel_component(request):
    return render(request, 'user_panel/components/side_panel.html', {})


@login_required
def shopping_panel(request):
    product_id = request.GET.get('product_id')
    operation = request.GET.get('operation')
    current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)
    order_edit = OrderDetail.objects.filter(products_id=product_id,order__user_id=request.user.id,order__is_paid=False).first()
    if order_edit is not None:
        if operation == 'add':
            order_edit.count =int(order_edit.count) + 1
            order_edit.save()
        if operation == '-':
            if int(order_edit.count) == 1:
                order_edit.delete()
            else:
                order_edit.count =int(order_edit.count)- 1
                order_edit.save()
        current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)
    total_price = current_order.get_total()
    context = {
        "total_price" : total_price,
        "current_order" : current_order
    }
    return render(request,'user_panel/shopping_panel.html',context)


@login_required
def delete_item_from_shopping(request):
    product_id = request.GET.get('product_id')
    if product_id is None:
        return JsonResponse({
            'status':'not_found'
        })
    
    current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)
    delete_count , delete_dict = current_order.orderdetail_set.all().filter(products_id= product_id).first().delete()
    if delete_count == 0:
        return JsonResponse({
            'status':'not_found_product'
        })

    total_price = current_order.get_total()
    context = {
        "total_price" : total_price,
        "current_order" : current_order
    }
    return render(request,'user_panel/shopping_panel.html',context)


# @login_required
# def payment_history(request):
#     active_order = Order.objects.filter(is_paid=True,user_id =request.user.id).first()
#     context = {
#         'historys':active_order
#     }
#     return render(request,'user_panel/payment_history.html',context)
