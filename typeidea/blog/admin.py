from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Post, Tag
from .adminforms import PostAdminForms
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

class PostInline(admin.TabularInline):  #可选择继承admin.StackenInline，以获取不同的展示样式

    fields = ('title', 'desc')
    extra = 1   # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines =  [PostInline]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')    #列表页展示的字段
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', )


@admin.register(Post, site=custom_site)
# @admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForms
    list_display = [
        'title', 'category', 'status', 'created_time', 'operator', 'owner'
    ]
    list_display_links =  []

    list_filter = [CategoryOwnerFilter, ]
    # filter_horizontal = ('category',)

    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    exclude = ('owner',)
    #编辑页面
    # fields = (
    #     # ('category', 'title'),    #小括号表示放在同一行
    #     'category',
    #     'title',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        (
            '基础配置', {
                'description': '基础配置描述',
                'fields': (
                    ('title', 'category'),
                    'status'
                ),
            }
        ),
        (
            '内容', {
                'fields': (
                    'desc',
                    'content',
                ),
            }
        ),
        (
            '额外信息', {
                'classes': ('collapse',),
                'fields': ('tag',),
            }
        )
    )

    # filter_horizontal =  ('tag',)
    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))   #这个是元组，后面有逗号
            reverse('cus_admin:blog_post_change', args=(obj.id,))   #这个是元组，后面有逗号
        )
    operator.short_description = '操作'


    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

















