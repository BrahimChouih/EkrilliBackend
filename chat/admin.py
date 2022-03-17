from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import (
    Message,
    Friend,
)

def userUrl(user):
    url = '/admin/accounts/account/%d/' % user.id
    return format_html('<a href="{}">{}</a>', url, user.email)



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'title', 'owner_', 'category', 'create_at')
    # list_display_links = ('id', 'title')
    # list_filter = ('category',)
    # search_fields = ('owner__email', 'title')

    # def owner_(self, obj):
    #     return userUrl(obj.owner)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'title', 'owner_', 'category', 'create_at')
    # list_display_links = ('id', 'title')
    # list_filter = ('category',)
    # search_fields = ('owner__email', 'title')

    # def owner_(self, obj):
    #     return userUrl(obj.owner)


