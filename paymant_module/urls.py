from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order',views.get_order,name='add_to_order'),
    path('request-payment/', views.send_request, name='request_payment'),
    path('verify-payment/', views.verify , name='verify_payment'),
]