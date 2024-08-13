from rest_framework import serializers
from .models import Message
from registration.serializer import UserModelDataSerializer
class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [ 'message']

class MessageAllModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        
        if request and request.method == "GET":
            fields['sender'] = UserModelDataSerializer()
            fields['receiver'] = UserModelDataSerializer()
        
        return fields