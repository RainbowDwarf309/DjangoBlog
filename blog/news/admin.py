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
    list_display = ('id', 'title', 'status', 'slug', 'author', 'category', 'created_at', 'get_photo', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'content', 'author', 'photo', 'get_photo', 'views', 'created_at',
              'link')
    list_editable = ('status',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Photo'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'get_photo')
    list_display_links = ('id', 'title')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Photo'


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

    mptt_indent_field = "id"

    list_display = ('id', 'user_submitter', 'post', 'status', 'text',)
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


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_subscribed', 'date')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('choices',)
    view_on_site = False


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type_of_news',)
    view_on_site = False


class ActionTrackAdmin(admin.ModelAdmin):
    list_display = ('date', 'ip', 'user', 'user_status', 'page', 'page_url', 'action', 'action_reason', "details",
                    'http_referer', "session_key", 'user_agent')
    list_display_links = ('date',)
    search_fields = ('ip', 'user__username', 'action_reason', 'details', "session_key", 'http_referer', 'user_agent')

    list_filter = ('page', 'action', 'action_reason', 'user_status')
    date_hierarchy = 'date'

    view_on_site = False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsType, NewsTypeAdmin)
admin.site.register(ActionTrack, ActionTrackAdmin)
