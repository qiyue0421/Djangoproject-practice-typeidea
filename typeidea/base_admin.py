# 抽象author基类
# 重写get_queryset方法和save_model方法
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):  # 通过继承admin.ModelAdmin实现对Model的增、删、改、查页面的配置
    """
    1.用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )  # 不展示owner字段

    def get_queryset(self, request):  # 当前用户只能查看自己的文章
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):  # 自动设置onwer
        obj.owner = request.user  # 自动设置当前登录的用户为作者，如果未登录则拿到的是匿名用户对象
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
