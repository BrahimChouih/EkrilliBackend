import json
from rest_framework.response import Response
from django.db.models import Count

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from chat.api.serializers import ChatItemSerializer, MessageSerializer
from chat import firebase_messaging_helper as firebaseMC

from chat.models import Message
from houses.api.serializers import OfferSerializer
from houses.models import Offer


# def pushNotification(message):

#     body = message.content_type
#     receiver = message.offer.owner.id
#     sender = message.user

#     if message.content_type == 'MESSAGE':
#         body = message.content

#     if message.message_type == 'RESPONSE':
#         receiver = message.user
#         sender = message.offer.house.owner

#     firebaseMC.pushNotification(
#         userId=receiver.id,
#         title=sender.username,
#         body=body,
#         notificationData=MessageSerializer(message, many=False).data,
#     )


class ChatPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 40


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    def getConversation(self, request, offerId, userId):
        try:
            Offer.objects.get(id=offerId)
        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)
        conversation = Message.objects.filter(offer=offerId, user=userId)
        page = self.paginate_queryset(conversation)
        # sleep(2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def getChatItem(self, request):
        messagesByUser = Message.objects.values('offer', 'user').filter(
            user__id=request.user.id).annotate(cont=Count('id'))

        messagesByOffer = Message.objects.values('offer', 'user').filter(
            offer__house__owner__id=request.user.id).annotate(cont=Count('id'))

        messages = messagesByOffer | messagesByUser
        serializer = ChatItemSerializer(messages, many=True)

        return Response(serializer.data)

    def getChatOfferSended(self, request, offerId, userId):
        messageAsList = Message.objects.filter(
            offer=offerId, user=userId, content_type='OFFER_INFO')
        if(len(messageAsList) == 0):
            return Response({'response': 'there isn\'t offer information here'})
        message = messageAsList[0]
        serialzer = MessageSerializer(message)
        offerSended = json.loads(message.message)

        data = {
            "message": serialzer.data,
            "start_date": offerSended["start_date"],
            "end_date": offerSended["end_date"],
        }
        
        return Response(data)

    def newMessageWithNewOffer(self, request, userId, *args, **kwargs):
        offerData = request.data['offer']
        offerData['user'] = request.user.id
        serializer = OfferSerializer(data=offerData)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'response': serializer.error_messages}, status=400)

        _mutable = True
        try:
            _mutable = request.data._mutable
            request.data._mutable = True
        except:
            pass

        request.data['offer'] = serializer.data['id']
        request.data['user'] = userId

        try:
            request.data._mutable = _mutable
        except:
            pass

        return super().create(request, *args, **kwargs)
        # response = super().create(request, *args, **kwargs)
        # if response.status_code == 200:
        #     message = Message.objects.get(id=response.data['id'])
        #     pushNotification(message)
        # return response

    def create(self, request, offerId, userId, *args, **kwargs):
        _mutable = True
        try:
            _mutable = request.data._mutable
            request.data._mutable = True
        except:
            pass

        request.data['offer'] = offerId
        request.data['user'] = userId

        try:
            request.data._mutable = _mutable
        except:
            pass
        try:
            offer = Offer.objects.get(id=offerId)
        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)

        if request.user.id != offer.house.owner.id and request.user.id != userId:
            return Response({'response': 'You dont have permision for that'}, status=400)

        return super().create(request, *args, **kwargs)
        # response = super().create(request, *args, **kwargs)
        # if response.status_code == 200:
        #     message = Message.objects.get(id=response.data['id'])
        #     pushNotification(message)
        # return response
