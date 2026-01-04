from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8,max_length=32,style={"input_type":"password"})
    confirm_password=serializers.CharField(write_only=True,min_length=8,max_length=32,style={"input_type":"password"})

    class Meta:
        model=CustomUser
        fields=['id','email','password','confirm_password']
        read_only_fields=['id']

    def validate(self,attrs):
        if attrs['password']!=attrs['confirm_password']:
            raise serializers.ValidationError({
                "message":"Passwords doesn't Match"
            })
        return attrs
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user=CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        user=authenticate(
            username=attrs['email'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        attrs['user']=user
        return attrs