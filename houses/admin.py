from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import (
    House,
    Picture,
    City,
    Municipality,
    Rating,
    Offer,
)


def userUrl(user):
    url = '/admin/accounts/account/%d/' % user.id
    return format_html('<a href="{}">{}</a>', url, user.email)


def houseUrl(house):
    url = '/admin/houses/house/%d/' % house.id
    return format_html('<a href="{}">{}</a>', url, house.title)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner_',)
    list_display_links = ('title',)
    # list_filter = ('municipality',)
    search_fields = ('title', 'id', 'owner__email', 'owner__username')

    def owner_(self, obj):
        return userUrl(obj.owner)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'house_',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    search_fields = ('id', 'house__title', 'house__id', )

    def house_(self, obj):
        return houseUrl(obj.house)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    # search_fields = ('sender__email',)

    # def owner_(self, obj):
    #     return userUrl(obj.semder)


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    # search_fields = ('sender__email',)

    # def owner_(self, obj):
    #     return userUrl(obj.semder)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    # search_fields = ('sender__email',)

    # def owner_(self, obj):
    #     return userUrl(obj.semder)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id',)
    # list_display_links = ('id',)
    # list_filter = ('city',)
    # search_fields = ('sender__email',)

    # def owner_(self, obj):
    #     return userUrl(obj.semder)
