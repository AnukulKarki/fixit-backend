from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializer import MessageModelSerializer, MessageAllModelSerializer
from django.db.models import Q
from django.db.models import OuterRef, Subquery
from registration.models import User
from registration.serializer import UserModelDataSerializer



class SendMessage(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            receiver = kwargs['id']
            serializer = MessageModelSerializer(data=request.data)
            if serializer.is_valid():
                messageData = request.data.get('message')
                Message.objects.create(sender_id = payload['user_id'], receiver_id = receiver, message = messageData)
                return Response({'msg':'Msg sent successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'login First'}, status=status.HTTP_401_UNAUTHORIZED)

class MessageList(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            messageList = distinct_users = set(Message.objects.filter(Q(sender=payload['user_id']) | Q(receiver=payload['user_id'])).values_list('sender__id', flat=True)) | \
                 set(Message.objects.filter(Q(sender=payload['user_id']) | Q(receiver=payload['user_id'])).values_list('receiver__id', flat=True))

            # Fetch user details for the distinct users
            users_communicated_with = User.objects.filter(id__in=distinct_users).exclude(id=payload['user_id'])
            
            serializer = UserModelDataSerializer(users_communicated_with, many = True, context = {'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'login First'}, status=status.HTTP_401_UNAUTHORIZED)

class MessageDetail(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            userId = kwargs['id']
            messageDetail = Message.objects.filter(Q(sender_id = userId , receiver_id = payload['user_id'] ) | Q(sender_id = payload['user_id'] , receiver_id =userId ) )
            messageDetail = messageDetail.order_by('created_at')
            serializer = MessageAllModelSerializer(messageDetail, many = True, context = {'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'login First'}, status=status.HTTP_401_UNAUTHORIZED)