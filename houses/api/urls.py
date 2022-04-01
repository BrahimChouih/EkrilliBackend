from rest_framework import routers
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
            'patch': 'partial_update',
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
            'get': 'getOffersForMyHouses',
            'post': 'create',
        }),
        name='offers'
    ),

    path(
        'offers-for-me/',
        OfferView.as_view({
            'get': 'getMyOffers',
        }),
        name='offers'
    ),

    path(
        'rating-on-house/',
        RatingView.as_view({
            'post': 'create',
        }),
        name='ratings'
    ),
    path(
        'ratings-of-house/<int:houseId>/',
        RatingView.as_view({
            'get': 'getHouseRatings',
        }),
        name='ratings'
    ),
]
router = routers.SimpleRouter()
router.register(r'offers',OfferView)

urlpatterns += router.urls