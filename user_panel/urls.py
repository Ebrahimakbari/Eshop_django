from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserPanelDashboard.as_view(),name='user_panel'),
    path('change-pass',views.ChangePasswordClass.as_view(),name='change_pass'),
    path('edit-profile',views.EditProfileClass.as_view(),name='edit_profile'),
    path('shopping-panel',views.shopping_panel,name='shopping_panel'),
    path('delete_item_shopping',views.delete_item_from_shopping,name='delete_item_shopping'),
    path('payment-history',views.PaymentHistory.as_view(),name='payment_history'),
    path('payment-detail',views.PaymentDetail.as_view(),name='payment_detail'),
]
