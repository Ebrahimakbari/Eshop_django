from datetime import datetime
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.shortcuts import render
from account_module .models import User
from project_module.models import product
from .models import Order,OrderDetail
from django.conf import settings
import requests
import json
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_order(request:HttpRequest):
    product_id = request.GET.get('product_id')
    product_count = request.GET.get('count')
    if request.user.is_authenticated:
        load_product = product.objects.filter(id=product_id,is_delete=False,is_active=True).first()
        if load_product is not None:
            current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)  
            current_order_detail = current_order.orderdetail_set.filter(products_id = product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += int(product_count)
                current_order_detail.save()
            else:
                new_order_detail = OrderDetail(products_id= product_id,count=product_count,order_id=current_order.id )
                new_order_detail.save()
            return JsonResponse({
                'status':'success',
                'text':'با موفقیت به سبد خرید اضافه شد',
                'icon':'success',
                'confirmText':'باشه ممنون'
            })
        else:
            return JsonResponse({
                'status':'not found',
                'text':'محصول مورد نظر موجود نیست',
                'icon':'warning',
                'confirmText':'باشه ممنون'
            })
    else:
        return JsonResponse({
            'status':'is not authenticated',
            'text':'برای خرید ابتدا وارد سایت شوید',
            'icon':'error',
            'confirmText':'ورود/ثبت نام'
    })


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'
    
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما"
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'

@login_required
def send_request(request):
    current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)
    amount = current_order.get_total()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount * 10,
        "Description": description,
        "CallbackURL": CallbackURL,
        "Phone": phone
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
            else:
                context = {'status': False, 'code': str(response['Status'])}
                return render(request,'paymant_module/payment_result.html',context)
        return response
    
    except requests.exceptions.Timeout:
        context = {'status': False, 'code': 'timeout'}
        return render(request,'paymant_module/payment_result.html',context)
    except requests.exceptions.ConnectionError:
        context = {'status': False, 'code': 'connection error'}
        return render(request,'paymant_module/payment_result.html',context)


@login_required
def verify(authority,request):
    current_order,created = Order.objects.get_or_create(is_paid = False ,user_id=request.user.id)
    amount = current_order.get_total()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_paid = False
            current_order.date = datetime.now()
            current_order.save()
            context = {'status': True, 'code': f'success payment with ref_id{response['RefID']}'}
            return render(request,'paymant_module/payment_result.html',context)
        else:
            context = {'status': False, 'code': 'payment canceled by customers'}
            return render(request,'paymant_module/payment_result.html',context)
    return response