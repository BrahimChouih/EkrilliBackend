from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from accounts.models import Account
from chat.models import Message
from houses.api.serializers import OfferSerializer
from houses.models import Offer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['offer'] = OfferSerializer(instance.offer).data
        rep['user'] = AccountSerializer(instance.user).data
        return rep

class ChatItemSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    offer = serializers.IntegerField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        offer = Offer.objects.get(id=instance['offer'])
        rep['offer'] = OfferSerializer(offer).data
        user = Account.objects.get(id=instance['user'])
        rep['user'] = AccountSerializer(user).data
        return rep

