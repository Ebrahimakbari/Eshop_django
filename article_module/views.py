from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from . import models
# Create your views here.


class ArticleListView(ListView):
    model = models.Article
    template_name = 'article_module/article_page.html'
    paginate_by = 1
    
    def get_queryset(self,**kwargs):
        query = super().get_queryset(**kwargs)
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(article_category__url_title__iexact = category_name)
        return query
        

def article_category_component(request: HttpRequest):
    article_category = models.ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,parent_id=None)
    context = {'main_categorys':article_category}
    return render(request,'article_module/article_component/article_category_component.html',context)


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = 'article_module/article_detail_page.html'
    def get_queryset(self,**kwargs):
        query =  super().get_queryset(**kwargs)
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article:models.Article = kwargs.get('object')
        context['comments'] = models.ArticleComment.objects.filter(article_id=article.id,parent=None).order_by('-created_date').prefetch_related('articlecomment_set')
        context['comments_count'] = models.ArticleComment.objects.filter(article_id=article.id).count()
        return context

def ArticleCommentAdd(request:HttpRequest):
    if request.user.is_authenticated:
        comment = request.GET.get('comment')
        parent_id = request.GET.get('parent_id')
        article_id = request.GET.get('article_id')
        new_comment = models.ArticleComment(text=comment,parent_id=parent_id,article_id=article_id,user_id=request.user.id)
        new_comment.save()
        context = {
            'comments': models.ArticleComment.objects.filter(article_id=article_id,parent=None).order_by('-created_date').prefetch_related('articlecomment_set'),
            'comments_count': models.ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/comments_include.html', context)
    return HttpResponse('response')