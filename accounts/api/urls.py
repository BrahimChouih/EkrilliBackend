from django.urls import path
from .views import registration_view, AccountView, LoginView
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'accounts'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('userinfo/<int:pk>/',
         AccountView.as_view({
             'get': 'userInfo',
             'post': 'updateUserInfo',
         }), name='userinfo'),
]
