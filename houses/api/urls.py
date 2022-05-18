from rest_framework import routers
from django.urls import path
from .views import (
    HouseView,
    CityView,
    MunicipalityView,
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
        'myhouses/',
        HouseView.as_view({
            'get': 'getMyHouses',
       
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
        'houses/picture/<int:pk>/',
        HouseView.as_view({
            'delete': 'deletePicture',
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
        'municipalities/<int:cityId>/',
        MunicipalityView.as_view({
            'get': 'list',
        }),
        name='municipalities'
    ),
    path(
        'offers/',
        OfferView.as_view({
            # 'get': 'getOffersForMyHouses',
            'get': 'list',
            'post': 'create',
        }),
        name='offers'
    ),

    path(
        'offers/city/<int:city>/',
        OfferView.as_view({
            'get': 'getOffersByCity',
        }),
        name='offers'
    ),

    path(
        'offers/<int:pk>/',
        OfferView.as_view({
            'get': 'getOfferInfo',
            'patch': 'partial_update',
        }),
        name='offers'
    ),

    path(
        'offers/status/<int:pk>/',
        OfferView.as_view({
            'patch': 'changeStatus',
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
router.register(r'offers', OfferView)

urlpatterns += router.urls
