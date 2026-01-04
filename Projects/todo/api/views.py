from django.shortcuts import render
from rest_framework import generics
from api.serializers import *
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer


class LoginView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user)

        return Response({
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        },status=status.HTTP_200_OK)

