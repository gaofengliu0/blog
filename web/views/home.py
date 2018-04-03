# -*- coding: UTF-8 -*-
from repository import models
from django.shortcuts import render,redirect
from utils.pagination import Pagination
from django.urls import reverse

def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    article_type_list = models.Article.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)

    else:
        article_type_id = None
        base_url = '/'

    data_count = article_list = models.Article.objects.filter(**kwargs).count()
    print(article_list,article_type_id,article_type_list)
    page_obj = Pagination(request.GET.get('p'),data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)
    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )


def test(request):

    page_obj = Pagination(request.GET.get('p'), 100)
    test_list = range(1,100)[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/test/')

    return render(
        request,
        'test.html',
        {
            'test_list':test_list,
            'page_str':page_str,
        }
    )
