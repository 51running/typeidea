from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Post, Tag
from .adminforms import PostAdminForms

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')    #列表页展示的字段
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

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

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForms
    list_display = (
        'title', 'category', 'status', 'created_time', 'operator', 'owner'
    )
    list_display_links =  []

    list_filter = [CategoryOwnerFilter]
    # filter_horizontal = ('category',)

    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    exclude = ('owner',)
    #编辑页面
    fields = (
        # ('category', 'title'),    #小括号表示放在同一行
        'category',
        'title',
        'desc',
        'status',
        'content',
        'tag',
    )

    # fieldsets = (
    #     (
    #         '基础配置', {
    #             'description': '基础配置描述',
    #             'fields': (
    #                 ('title', 'category'),
    #                 'status'
    #             ),
    #         }
    #     ),
    #     (
    #         '内容', {
    #             'fields': (
    #                 'desc',
    #                 'content',
    #             ),
    #         }
    #     ),
    #     (
    #         '额外信息', {
    #             'classes': ('collapse',),
    #             'fields': ('tag',),
    #         }
    #     )
    # )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))   #这个是元组，后面有逗号
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        print(qs)
        return qs.filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

















