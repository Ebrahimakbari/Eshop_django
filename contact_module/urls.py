from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('profilePic/', views.ProfilePicView.as_view(), name='profile_pic'),
    path('profileListPic/', views.ProfileListView.as_view(), name='profileList_pic'),
]