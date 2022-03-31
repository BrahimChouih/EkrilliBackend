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
            'get': 'list',
        }),
        name='houses'
    ),
]
