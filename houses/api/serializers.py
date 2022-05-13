from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from houses.models import (
    House,
    Picture,
    City,
    Municipality,
    Offer,
    Rating,
)


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['owner'] = AccountSerializer(instance.owner).data
        rep['municipality'] = MunicipalitySerializer(instance.municipality).data
        pictures = Picture.objects.filter(house=instance.id)
        rep['pictures'] = PictureSerializer(pictures, many=True).data
        return rep


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        # exclude = ('',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        # exclude = ('',)

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'
        # exclude = ('',)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['city'] = CitySerializer(instance.city).data
        return rep


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['house'] = HouseSerializer(instance.house).data
        rep['user'] = AccountSerializer(instance.user).data
        return rep


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        # exclude = ('',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['offer'] = OfferSerializer(instance.offer).data
        return rep
