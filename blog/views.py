from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from config.models import *
from django.views.generic import ListView, DetailView
# Create your views here.


# 类视图实现
class CommonViewMixin:  # 一些基础通用数据：分类导航、侧边栏、底部导航
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):  # 首页
    queryset = Post.latest_posts()  # 此处设置了queryset，所以该类的方法get_queryset()会直接返回queryset(即Post)
    paginate_by = 5  # 每页数据
    context_object_name = 'post_list'  # queryset名
    template_name = 'blog/list.html'  # 模板名


class CategoryView(IndexView):  # 分类列表页
    def get_context_data(self, **kwargs):  # 重写get_context_data方法，用来获取上下文数据并最终将其传入模板
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')  # kwargs中的数据其实是从URL定义中拿到的
        category = get_object_or_404(Category, pk=category_id)  # 获取一个对象的实例，如果获取到则返回，如果不存在抛出404错误
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):  # 重写get_queryset方法，根据分类过滤
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):  # 标签列表页
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):  # 重写get_queryset方法，根据标签过滤
        queryset = super().get_queryset()  # 调用父类get_queryset方法，得到Post表
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)  # 查询Post表，约束条件为tag_id，此处使用了连表操作


class PostDetailView(CommonViewMixin, DetailView):  # 文章详情页
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'  # pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询


# 函数视图实现
"""
def post_list(request, category_id=None, tag_id=None):  # 使用Model从数据库中批量拿取数据，然后把标题和摘要展示到页面上
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())  # 将键值对更新到字典
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):  # 展示一条文章数据
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
"""