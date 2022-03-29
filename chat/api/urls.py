from django.urls import path
from .views import MessageView


app_name = 'chat'

urlpatterns = [
    path('chat/',
         MessageView.as_view({
             'get': 'list',
         }), name='chat'),
]
