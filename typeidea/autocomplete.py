# 配置所有需要自动补全的接口，实质上是自动补全的View层
from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():  # 判断用户是否登录，如果没有登录则返回空的queryset
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)  # 获取当前用户创建的所有分类

        if self.q:  # q指url上传递过来的值
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
