

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import  Badge, BadgeAssign
from registration.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from blacklist.models import Blacklist
from datetime import datetime
from gighire.models import GigProposal, Rating
from proposal.models import Proposal
from registration.utils import verify_access_token
from gighire.models import Rating, GigProposal
from django.db.models import Q

def badgeAssign(userId, role):
    user = User.objects.get(id =userId)
    RatingObj = Rating.objects.filter(rateduser_id = user.id)
    count = 0
    for i in RatingObj:
        if i.rate == 5:
            count += 1
    if count >= 3:
        badge = Badge.objects.get(name = "perfectionist")
        a = BadgeAssign.objects.filter(user = user, Badge = badge)
        if len(a) == 0:
            BadgeAssign.objects.create(user = user, Badge = badge)

    if role.lower() == "worker":
        gighireproposal = GigProposal.objects.filter(worker = user).filter(Q(status = "accept") | Q(status = "completed") | Q(status = "started") | Q(status = "payed"))
        job = Proposal.objects.filter(worker = user).filter(Q(status = "accept") | Q(status = "completed") | Q(status = "started") | Q(status = "payed"))
        count = len(gighireproposal) + len(job)
        if count >= 5:
            badge = Badge.objects.get(name = "workaholic")
            a = BadgeAssign.objects.filter(user = user, Badge = badge)
            if len(a) == 0:
                BadgeAssign.objects.create(user = user, Badge = badge)
    return True