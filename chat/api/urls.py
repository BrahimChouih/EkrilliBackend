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

    path(
        'chat/items/',
        MessageView.as_view({
            'get': 'getChatItem',
        }),
        name='chat'
    ),

    path(
        'chat/offer/sended/<int:offerId>/<int:userId>/',
        MessageView.as_view({
            'get': 'getChatOfferSended',
        }),
        name='chat'
    ),

]
