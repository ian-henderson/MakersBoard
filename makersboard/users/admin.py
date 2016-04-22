from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined']
    list_editable = ['email']
    list_display_links = ['date_joined']
    search_fields = ['username', 'email']

    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
