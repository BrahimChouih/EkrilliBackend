from django.forms import model_to_dict
from django.db.models import Q
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
        page = self.paginate_queryset(House.objects.filter(isAvailable=True))
        # sleep(2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def getHouseByCity(self, request, city):
        houses = House.objects.filter(city=city, isAvailable=True)
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
            return Response({'response': 'There is not any house with this id'}, status=404)
        serializer = HouseSerializer(house, many=False)
        return Response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        try:
            house = House.objects.get(id=pk)
        except:
            return Response({'response': 'There is not a house with this id'}, status=404)
        if house.owner.id != request.user.id:
            return Response({'response': 'You dont have permision for that'}, status=400)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            house = House.objects.get(id=pk)
        except:
            return Response({'response': 'There is not an item with this id'}, status=404)
        if house.owner.id == request.user.id:
            super().destroy(request, pk, *args, **kwargs)
            return Response({'response': 'Successfully delete this item'})
        else:
            return Response({'response': 'You dont have permision for that'}, status=400)


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class OfferView(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def getOffersForMyHouses(self, request):
        offers = Offer.objects.filter(house__owner__id=request.user.id)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=200)

    def getMyOffers(self, request):
        # offers = Offer.objects.filter(user=request.user.id)
        offers = Offer.objects.filter(
            Q(user=request.user.id) | Q(house__owner__id=request.user.id))
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=200)

    def getOfferInfo(self, request, pk, *args, **kwargs):
        try:
            offer = Offer.objects.get(id=pk)
        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)
        serializer = OfferSerializer(offer, many=False)
        return Response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        try:
            offer = Offer.objects.get(id=pk)
        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)

        if request.user.id == offer.house.owner.id or request.user.id == offer.user.id:
            return super().partial_update(request, *args, **kwargs)

        return Response({'response': 'You dont have permision for that'}, status=400)

    def changeStatus(self, request, pk, *args, **kwargs):
        try:
            offer = Offer.objects.get(id=pk)
        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)

        if request.user.id == offer.house.owner.id or request.user.id == offer.user.id:
            status = request.data['status']
            offer.status = status
            print(type(offer.__dict__))
            serializer = OfferSerializer(data=model_to_dict(offer))
            if(serializer.is_valid()):
                offer.save()
                return Response({'response': 'change status value to %s' % status}, status=200)
            return Response(serializer.error_messages, status=400)

        return Response({'response': 'You dont have permision for that'}, status=400)


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def getHouseRatings(self, request, houseId):
        try:
            House.objects.get(id=houseId)
        except:
            return Response({'response': 'There is not a house with this id'}, status=404)
        ratings = Rating.objects.filter(offer__house__id=houseId)
        page = self.paginate_queryset(ratings)
        # sleep(2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            offer = Offer.objects.get(id=request.data['offer'])

        except:
            return Response({'response': 'There is not any offer with this id'}, status=404)

        try:
            Rating.objects.get(offer=offer.id, offer__user__id=request.user.id)
            return Response({'response': 'You are already rate this offer'}, status=400)
        except:
            pass

        if(offer.id != request.user.id):
            return Response({'response': 'You dont have permision for that'}, status=400)

        return super().create(request, *args, **kwargs)
