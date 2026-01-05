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


class CreateListTaskView(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TaskSerializer

    # All users will see all Tasks
    # def get_queryset(self):
    #     return super().get_queryset()
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class RetrieveUpdataeDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
