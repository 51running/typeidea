# from django.http import HttpResponse
from django.shortcuts import render

from .models import Post, Tag, Category
from config.models import SiderBar

from django.views.generic import DetailView

def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_post()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SiderBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        post = None
    context = {
        'post': post,
        'sidebars': SiderBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail'










