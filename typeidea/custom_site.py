# 用户模块的管理与文章分类等数据的管理分开
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):  # 继承AdminSite用来自定义site
    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'


custome_site = CustomSite(name='cus_admin')
