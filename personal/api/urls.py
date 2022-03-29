from django.urls import path
from .views import FavoriteView


app_name = 'personal'

urlpatterns = [
    path('favorites/',
         FavoriteView.as_view({
             'get': 'list',
         }), name='favorites'),
]
