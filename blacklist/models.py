from django.db import models
from registration.models import User

# Create your models here.

class Blacklist(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name = "blaclistuser")
