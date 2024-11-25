from django.urls import path
from . import views

urlpatterns = [
    path('',views.ArticleListView.as_view(), name='article_page' ),
    path('cat/<str:category>',views.ArticleListView.as_view(), name='article_category_component' ),
    path('comment-add',views.ArticleCommentAdd, name='article_comment_add' ),
    path('<pk>/',views.ArticleDetailView.as_view(), name='article_detail' ),
]
