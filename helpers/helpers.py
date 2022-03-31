
from houses.api.serializers import (
    CitySerializer,
    HouseSerializer,
    PictureSerializer
)
from houses.models import (
    Picture
)
from accounts.api.serializers import (
    AccountSerializer
)
from personal.api.serializers import FavoriteSerializer


def userToJson(user):
    data = AccountSerializer(user, many=False).data
    return data


def houseToJson(house):
    data = HouseSerializer(house, many=False).data
    data['owner'] = userToJson(house.owner)
    data['city'] = CitySerializer(
        house.city, many=False).data
    data['pictures'] = PictureSerializer(
        Picture.objects.filter(house=house.id),
        many=True,
    ).data
    return data

def favoriteToJson(favorite):
    data = FavoriteSerializer(favorite,many=False).data
    data['house']=houseToJson(favorite.house)
    return data
