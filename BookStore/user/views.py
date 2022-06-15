from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from utils import encode_token, decode_token


class UserDetailAPI(APIView):
    def get(self, request, *args, **kwargs):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(id=user_id)
        print(user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print("hiiii", user)
        if not user:
            return Response({'Error': 'Check your username and password', 'Code': 401})
        login(request, user)
        token = encode_token(user)
        return Response({"message": "user logged in", 'token': token, "status": status.HTTP_200_OK})


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response({'Message': 'You are Logged Out', "status": status.HTTP_200_OK})
