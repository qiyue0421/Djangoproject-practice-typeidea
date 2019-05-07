from django.contrib import admin
from comment.models import *
from typeidea.custom_site import custome_site

# Register your models here.
@admin.register(Comment, site=custome_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
