from django.contrib import admin
from django import forms
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from .models import *


# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Post
#         fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'content', 'author', 'photo', 'get_photo', 'views', 'created_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

    mptt_indent_field = "id"

    list_display = ('id', 'user_submitter', 'status', 'text',)
    list_display_links = ('id', 'text')
    list_editable = ('status',)
    search_fields = ('id', 'user_submitter__username', 'text')
    view_on_site = False
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
        'status',
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'karma')
    search_fields = ('user__username', 'user__email')
    view_on_site = False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
