from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.api.serializers import RegistrationSerializer, AccountSerializer
from accounts.models import Account


@api_view(['POST', ])
@permission_classes((AllowAny,))
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if request.method == 'POST':
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registrated a new user.'
            data['email'] = account.email
            data['username'] = account.username

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            return Response(serializer.errors,status=400)
            
        return Response(data,status=200)
    return Response(serializer.data)


class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def userInfo(self, request, pk):
        if(pk == 0):
            account = request.user
        else:
            account = Account.objects.get(id=pk)
        data = AccountSerializer(account, many=False).data
        return Response(data)

    def updateUserInfo(self, request, pk, *args, **kwargs):
        if(pk != request.user.id):
            return Response({'response': 'this is not your account'}, status=400)

        usernames = []
        for i in Account.objects.all():
            usernames.append(i.username.lower())

        try:
            if(request.data['username'].lower() in usernames):
                return Response({"username": ["account with this username already exists."]}, status=400)
        except:
            print('')

        return super().partial_update(request, pk, *args, **kwargs)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        _mutable = True
        try:
            _mutable = request.data._mutable
            request.data._mutable = True
        except:
            pass

        request.data['username'] = request.data['email']

        try:
            request.data._mutable = _mutable
        except:
            pass

        return super().post(request, *args, **kwargs)
