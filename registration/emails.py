from django.core.mail import send_mail
import random
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, VerificationCode
from datetime import datetime, timedelta

#Testing Method
class sendEmail(APIView):
    def get(self, request):
        subject = "Account Verification Email"
        otp = random.randint(1000, 9999)
        message = f"Your OTP is {otp}"
        email_from = settings.EMAIL_HOST
        email = "np01cp4a210134@islingtoncollege.edu.np"
        send_mail(subject, message, email_from, [email])
        return Response({"message": "Email Sent"}, status=status.HTTP_200_OK)
    

def sendVerificationEmail(email):
    subject = "Account Verification Email"
    otp = random.randint(1000, 9999)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST
    try:
        userId = User.objects.get(email=email).id
    except:
        return False
    now = datetime.now()

    five_minutes_later = now + timedelta(minutes=5)
    VerificationCode.objects.create(code=otp, user_id=userId, expired=five_minutes_later)
    try:
        send_mail(subject, message, email_from, [email])
        return True
    except:
        return False
    
def sendConfirmationEmail(email, name, jobTitle, phone, emailClient):
    subject = "Job Accepted"
    message = f"Your Job Reques was accepted\nWork Details\nClient: {name} \nJob Title: {jobTitle} \nPhone: {phone}\nEmail: {emailClient}\nThank You!"
    email_from = settings.EMAIL_HOST
    try:
        send_mail(subject, message, email_from, [email])
        return True
    except:
        return False
