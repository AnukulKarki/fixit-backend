
from rest_framework.views import APIView
from .models import  Badge, BadgeAssign
from rest_framework.response import Response
from rest_framework import status
from registration.utils import verify_access_token
from django.db.models import Q
from .badge import badgeAssign
from .serializer import BadgeAssignModelSerializer
from registration.models import User
# Create your views here.

class BadgeView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')
        verification, payload = verify_access_token(token)
        if verification:
            response = badgeAssign(payload['user_id'], payload['role'])
            badgeData = BadgeAssign.objects.filter(user_id = payload['user_id'])
            serializer = BadgeAssignModelSerializer(badgeData, many = True, context = {"request": request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response("Invalid Token", status = status.HTTP_400_BAD_REQUEST)

class BadgeViewData(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        User = User.objects.get(id = id)
        Response = badgeAssign(User.id, User.role)
        badgeData = BadgeAssign.objects.filter(user_id = id)
        serializer = BadgeAssignModelSerializer(badgeData, many = True, context = {"request": request})
        return Response(serializer.data, status = status.HTTP_200_OK)