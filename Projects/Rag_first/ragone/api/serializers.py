from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8,max_length=32,style={'input_type':'password'})
    confirm_password=serializers.CharField(write_only=True,min_length=8,max_length=32,style={'input_type':'password'})

    class Meta:
        model=CustomUser
        fields=['email','password','confirm_password']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"message":"Password's didn't match"})
        return attrs

    def create(self,validated_data):
        validated_data.pop('confirm_password')

        user=CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email']
    
    #DRF calls create() automatically when you call .save() on the serializer
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        user=authenticate(
            username=attrs['email'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user']=user
        return attrs
    

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields=["id","name","file"]
        read_only_fields=["id"]
   # DRF automatically calls validation methods during serializer.is_valid()(this line is in views):
# 1. For each field, if validate_<fieldname>() exists → it is called
#    e.g. validate_name(), validate_file()
# 2. Then validate(self, attrs) is called (object-level validation)
# 3. Only if all validations pass → serializer.save() is executed

    # def validate_name(self,value):
    #     print(f"name= {value}")
    #     return value

    def validate_file(self, file):
        if not file.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Upload PDF files only")

        
        if file.content_type != "application/pdf":
            raise serializers.ValidationError("Invalid file type")

        return file

    def create(self,validated_data):
        user=self.context["request"].user
        return Document.objects.create(user=user,**validated_data)
    
class QuestionSerializer(serializers.Serializer):
    question=serializers.CharField()

class YoutubeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=YoutubeVideo
        fields=['id','name','url']
        read_only_fields=['id']
        # write_only_fields=['url']
        extra_kwargs={
            'url':{
                'write_only':True
            }
        }
    def validate_url(self,value):
        if "youtube.com" not in value and "youtu.be" not in value:
            raise serializers.ValidationError("Invalid Youtube URL")
        return value
        
