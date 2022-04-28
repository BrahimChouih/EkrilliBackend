from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from houses.api.serializers import HouseSerializer, OfferSerializer
from personal.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
       rep = super().to_representation(instance)
       rep['user'] = AccountSerializer(instance.user).data
       rep['offer'] = OfferSerializer(instance.offer).data
       return rep
