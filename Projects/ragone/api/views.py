from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import *

class RegisterView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "message":"User Registered Successfully",
            "user_id":user.id,
            "user_name":user.username
        },status=status.HTTP_201_CREATED)

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
    
    """
Input data (request.data)
        ↓
serializer.is_valid()
        ↓
    - Check individual fields
    - Call validate()
        ↓
serializer.validated_data
        ↓
View can use validated_data['user'], etc.
    """


class DocumentUploadView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
        serializer=DocumentUploadSerializer(
            data=request.data,
            context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        document=serializer.save()
        return Response({
            "id":document.id,
            "name":document.name,
            "message":"pdf uploaded successfully"
        },status=status.HTTP_201_CREATED)
