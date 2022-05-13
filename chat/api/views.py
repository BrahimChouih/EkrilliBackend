from turtle import title
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token
from django.db.models import Count

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from chat.api.serializers import MessageSerializer
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


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

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

    def getOffersByMessages(self, request):
        offersIds = Message.objects.values('offer').filter(user__id=request.user.id).annotate(cont=Count('id'))
        offersIds = list(offersIds)
        offers = Offer.objects.filter(id__in=[i['offer'] for i in offersIds])
        serializer = OfferSerializer(offers,many=True)
        return Response(serializer.data)

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
