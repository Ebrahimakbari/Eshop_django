from django.urls import path
from account_module.views import RegisterView, LoginView, ActivateAccount, ResetView, ResetPassView, LogoutView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register_page' ),
    path('login/',LoginView.as_view(),name='login_page' ),
    path('logout/',LogoutView.as_view(),name='logout_page' ),
    path('reset_page/',ResetView.as_view(),name='reset_page' ),
    path('reset_password/<email_activate_code>',ResetPassView.as_view(),name='reset_password_page' ),
    path('activate_account/<activate_code>',ActivateAccount.as_view(),name='activate_account' ),
]