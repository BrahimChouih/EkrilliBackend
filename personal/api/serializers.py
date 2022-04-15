from rest_framework import serializers
from houses.api.serializers import HouseSerializer
from personal.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
       rep = super().to_representation(instance)
       rep['house'] = HouseSerializer(instance.house).data
       return rep
