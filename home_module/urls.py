from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeIndexView.as_view(),name='home_index'),
    path('about-us', views.AboutUs.as_view(),name='about_us'),
    ]