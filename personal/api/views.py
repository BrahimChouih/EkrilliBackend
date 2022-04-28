from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from personal.api.serializers import FavoriteSerializer

from personal.models import Favorite


class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        _mutable = True
        try:
            _mutable = request.data._mutable
            request.data._mutable = True
        except:
            pass

        request.data['user'] = request.user.id

        try:
            request.data._mutable = _mutable
        except:
            pass
        try:
            Favorite.objects.get(
                user=request.user.id, offer=request.data['offer'])
            return Response({
                'response': 'This offer already exist in your favorite'}, status=400)
        except:
            return super().create(request, *args, **kwargs)

    def getMyFavorite(self, request, *args, **kwargs):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data, status=200)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            favotite = Favorite.objects.get(id=pk)
        except:
            return Response({'response': 'There is not any item with this id'}, status=404)
        if favotite.user.id == request.user.id:
            super().destroy(request, pk, *args, **kwargs)
            return Response({'response': 'Successfully delete this item'})
        else:
            return Response({'response': 'You dont have permision for that'}, status=400)
