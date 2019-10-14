# from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_list_or_404

from .models import Post, Tag, Category
from config.models import SiderBar

from django.views.generic import DetailView, ListView

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


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#
# class PostListView(ListView):
#     queryset = Post.latest_post()
#     paginate_by = 2
#     context_object_name = 'post_list'   # 如果不设置此项，在模板中需要使用object_list变量
#     template_name = 'blog/list.html'


class CommonViewMinxin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SiderBar.get_all()
        })
        context.update(Category.get_navs())
        print(dir(context['paginator']))
        return context


class IndexView(CommonViewMinxin, ListView):
    queryset = Post.latest_post()
    paginate_by = 2
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'


class PostDetailView(CommonViewMinxin, DetailView):
    queryset = Post.latest_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_list_or_404(Category, pk=category_id)
        context.update({
            'catergory': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_list_or_404(Category, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        tag = self.kwargs.get('tag')
        return queryset.filter(tag_id=tag)





