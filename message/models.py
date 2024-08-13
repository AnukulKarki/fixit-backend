from django.db import models
from registration.models import User
import datetime

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now(), null=True)
    
        
    

