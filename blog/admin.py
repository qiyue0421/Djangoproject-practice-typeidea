from django.contrib import admin
from blog.models import *
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # 通过继承admin.ModelAdmin实现对Model的增、删、改、查页面的配置
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')  # 后台展示字段
    fields = ('name', 'status', 'is_nav')   # 可添加字段

    def save_model(self, request, obj, form, change):  # 自动设置onwer
        obj.owner = request.user   # 自动设置当前登录的用户为作者，如果未登录则拿到的是匿名用户对象
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):  # 展示分类下有多少篇文章
        return obj.post_set.count()  # 使用聚合查询

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'operator']  # 注意此处的operator是自定义的方法
    fields = (('category', 'title'), 'desc', 'status', 'content', 'tag')
    list_display_links = []
    list_filter = ['category']  # 过滤器
    search_fields = ['title', 'category__name']  # 搜索字段
    actions_on_top = True  # 动作相关的配置展示在顶部
    # actions_on_bottom = True  # 动作相关的配置展示在底部
    # save_on_top = True  # 保存、编辑、编辑并新建按钮是否在顶部展示

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,)))  # reverse根据名字解析出url

    operator.short_description = '操作'  # 指定表头的展示文案

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
