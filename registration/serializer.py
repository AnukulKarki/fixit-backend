from rest_framework import serializers
from .models import *
from category.serializer import CategoryModelSerializer

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserModelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','firstname','lastname','citizenship_no','email','phone','age','district','city','street_name','rating','category','role', 'profileImg','image','isKycVerified' ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        
        if request and request.method == "GET":
            fields['category'] = CategoryModelSerializer()
        
        return fields

class ValidationCodeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['code']