from rest_framework import serializers
from .models import Blacklist
from registration.serializer import UserModelDataSerializer

class BlacklistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = ['id','user']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        
        if request and request.method == "GET":
            fields['user'] = UserModelDataSerializer()
        
        return fields