from django.db import models
from registration.models import User

# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BadgeAssign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Badge = models.ForeignKey(Badge, on_delete=models.CASCADE)