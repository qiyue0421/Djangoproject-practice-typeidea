import xadmin
from django.contrib import admin
from blog.models import *  # 引入数据库
from django.urls import reverse
from django.utils.html import format_html
from blog.adminforms import PostAdminForm  # 自定义后台管理表单
from typeidea.custom_site import custome_site  # 自定义站点
from typeidea.base_admin import BaseOwnerAdmin  # 抽象出author基类
from django.contrib.admin.models import LogEntry  # 引入操作日志
from xadmin.layout import Row, Fieldset, Container  # 使用xadmin布局
from xadmin.filters import manager, RelatedFieldListFilter


# Register your models here.
class PostInline:  # 关联文章内容
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 2  # 控制的数量
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')  # 后台展示字段
    fields = ('name', 'status', 'is_nav')   # 可添加字段
    inlines = [PostInline, ]  # 设置在分类页面直接编辑关联的文章

    def post_count(self, obj):  # 展示分类下有多少篇文章
        return obj.post_set.count()  # 使用聚合查询

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


"""
class CategoryOwnerFilter(admin.SimpleListFilter):  # 自定义过滤器只展示当前用户创建的分类
    # 两个属性：
    title = '分类过滤器'  # 展示标题
    parameter_name = 'owner_category'  # 查询时URL参数的名字 比如查询分类id为1的内容时，URL后面的Query部分是 '?owner_category=1'

    # 两个方法：
    def lookups(self, request, model_admin):  # 返回要展示的内容和查询时用的id
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):  # 根据URL Query的内容返回列表页数据
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())  # 根据id过滤queryset(展示数据的合集)
        return queryset
"""


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):  # 确认字段是否需要被当前的过滤器处理
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)  # 注册使用自定义的后台管理站点
class PostAdmin(BaseOwnerAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']  # 注意此处的operator是自定义的方法
    # exclude = ('owner',)  # 不展示owner字段

    """
    # fields = (('category', 'title'), 'desc', 'status', 'content', 'tag')
    fieldsets = (  # 控制页面布局
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category',),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc', 'content',
            ),
        }),
        ('额外信息', {
            'fields': ('tag',),
        })
    )
    filter_horizontal = ('tag',)  # 针对多对多字段的展示,水平布局
    # filter_vertical = ('tag',)  # 垂直布局
    """

    list_display_links = []
    list_filter = ['category']  # 过滤器——使用的自定义过滤器：只看自己创建的分类
    search_fields = ['title', 'category__name']  # 搜索字段
    actions_on_top = True  # 动作相关的配置展示在顶部
    # actions_on_bottom = True  # 动作相关的配置展示在底部
    # save_on_top = True  # 保存、编辑、编辑并新建按钮是否在顶部展示

    form = PostAdminForm  # 使用自定义的后台表单

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,)))  # reverse根据名字解析出url

    operator.short_description = '操作'  # 指定表头的展示文案

    class Media:  # 自定义Media类，增加想要添加的JavaScript以及CSS资源
        css = {'all': ("https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css", ), }
        js = ('https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js', )

    # def get_media(self):
    # # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
    # media = super().get_media()
    # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    # media.add_css({
    # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    # })
    # return media


"""
@admin.register(LogEntry, site=custome_site)
class LogEntryAdmin(admin.ModelAdmin):  # 操作日志
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
"""
