from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import (
    Message,
)


def userUrl(user):
    url = '/admin/accounts/account/%d/' % user.id
    return format_html('<a href="{}">{}</a>', url, user.email)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    # search_fields = ('sender__email',)

    # def owner_(self, obj):
    #     return userUrl(obj.semder)
