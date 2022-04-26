from django.urls import path
from .views import MessageView


app_name = 'chat'

urlpatterns = [
    path(
        'conversation/<int:offerId>/<int:userId>/',
        MessageView.as_view({
            'get': 'getConversation',
            'post': 'create',
        }),
        name='chat'
    ),  
    path(
        'new-message/new-offer/<int:userId>/',
        MessageView.as_view({
            'post': 'newMessageWithNewOffer',
        }),
        name='new message'
    ),

]
