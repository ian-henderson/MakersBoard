from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'timestamp']
    list_editable = ['title']
    list_display_links = ['timestamp']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'description']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
