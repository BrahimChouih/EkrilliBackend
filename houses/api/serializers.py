from rest_framework import serializers
from houses.models import House


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
        # exclude = ('',)
