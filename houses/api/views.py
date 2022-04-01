from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

from houses.api.serializers import (
    HouseSerializer,
    PictureSerializer,
    CitySerializer,
    OfferSerializer,
    RatingSerializer,
)

from houses.models import (
    House,
    Picture,
    City,
    Offer,
    Rating,
)


class HouseView(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]

    def getHouses(self, request):
        page = self.paginate_queryset(self.queryset)
        # sleep(2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def getHouseByCity(self, request, city):
        houses = House.objects.filter(city=city)
        page = self.paginate_queryset(houses)
        # sleep(2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def createWithImages(self, request, *args, **kwargs):
        _mutable = True
        try:
            _mutable = request.data._mutable
            request.data._mutable = True
        except:
            pass

        request.data['owner'] = request.user.id

        try:
            request.data._mutable = _mutable
        except:
            pass
        data = super().create(request, *args, **kwargs).data

        for i in range(len(request.FILES)):
            Picture.objects.create(
                house_id=data['id'], image=request.FILES[f'pictures[{i}][picture]'])
        return Response(data)

    def getHouseInfo(self, request, pk, *args, **kwargs):
        try:
            house = House.objects.get(id=pk)
        except:
            return Response({'response': 'There is not a house with this id'}, status=400)
        serializer = HouseSerializer(house, many=False)
        return Response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        try:
            house = House.objects.get(id=pk)
        except:
            return Response({'response': 'There is not a house with this id'}, status=400)
        if house.owner.id != request.user.id:
            return Response({'response': 'You dont have permision for that'}, status=400)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            house = House.objects.get(id=pk)
        except:
            return Response({'response': 'There is not an item with this id'}, status=400)
        if house.owner.id == request.user.id:
            super().destroy(request, pk, *args, **kwargs)
            return Response({'response': 'Successfully delete this item'})
        else:
            return Response({'response': 'you don\'t have permission for this'}, status=400)



class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class OfferView(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
