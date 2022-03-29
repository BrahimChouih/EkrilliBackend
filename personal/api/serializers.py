from rest_framework import serializers
from personal.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        # exclude = ('',)
