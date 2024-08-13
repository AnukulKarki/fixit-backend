from django.urls import path
from .views import SendMessage, MessageList, MessageDetail
urlpatterns = [
     path('send/<int:id>/',  SendMessage.as_view() ),  #id refers to receiver id
     path('list/',  MessageList.as_view() ),  #
     path('detail/<int:id>/',  MessageDetail.as_view() ),  #
]