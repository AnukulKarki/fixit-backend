from rest_framework import serializers
from .models import BadgeAssign, Badge
from registration.serializer import UserModelDataSerializer

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"

class BadgeAssignModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeAssign
        fields = "__all__"
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        
        if request and request.method == "GET":
            fields['user'] = UserModelDataSerializer()
            fields['Badge'] = BadgeSerializer()

        
        return fields