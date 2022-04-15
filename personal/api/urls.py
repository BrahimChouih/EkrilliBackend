from django.urls import path
from .views import FavoriteView


app_name = 'personal'

urlpatterns = [
    path('favorites/', FavoriteView.as_view({
        'get': 'getMyFavorite',
        'post': 'create',
    })),
    path('favorites/<int:pk>/', FavoriteView.as_view({
        'delete': 'destroy',
    })),
]
