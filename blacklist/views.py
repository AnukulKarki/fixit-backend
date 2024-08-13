from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from .serializer import BlacklistModelSerializer
from .models import Blacklist

# Create your views here.

class BlacklistAddView(APIView):
    def get(self, request,  *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                userid = kwargs['id']
                if len(Blacklist.objects.filter(user_id = userid)) > 0:
                    return Response({'msg':'User is already in black list'}, status=status.HTTP_400_BAD_REQUEST)

                Blacklist.objects.create(user_id = userid)
                return Response({'msg':'User is now blacklisted'}, status=status.HTTP_200_OK)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class BlacklistRemoveView(APIView):
    def get(self, request,  *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                userid = kwargs['id']
                if len(Blacklist.objects.filter(user_id = userid)) == 0:
                    return Response({'msg':'User not Found'}, status=status.HTTP_400_BAD_REQUEST)
                Blacklist.objects.filter(user_id = userid).delete()
                return Response({'msg':'User is now removed from blacklist'}, status=status.HTTP_200_OK)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class BlacklistListView(APIView):
    def get(self, request):
        blacklistData = Blacklist.objects.all()
        serializer = BlacklistModelSerializer(blacklistData, many = True, context = {'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

