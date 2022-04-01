from django.urls import path
from .views import (
    HouseView,
    CityView,
    OfferView,
    RatingView,
)


app_name = 'houses'

urlpatterns = [
    path(
        'houses/',
        HouseView.as_view({
            'get': 'getHouses',
            'post': 'createWithImages',
        }),
        name='houses'
    ),
    path(
        'houses/<int:pk>/',
        HouseView.as_view({
            'get': 'getHouseInfo',
            'put': 'partial_update',
            'delete': 'destroy',
        }),
        name='houses'
    ),
    path(
        'houses/city/<int:city>/',
        HouseView.as_view({
            'get': 'getHouseByCity',
        }),
        name='houses'
    ),
    path(
        'cities/',
        CityView.as_view({
            'get': 'list',
        }),
        name='cities'
    ),
    path(
        'offers/',
        OfferView.as_view({
            'get': 'list',
        }),
        name='offers'
    ),
    path(
        'ratings/',
        RatingView.as_view({
            'get': 'list',
        }),
        name='ratings'
    ),
]
