from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from chat.models import Message
from houses.api.serializers import OfferSerializer


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
