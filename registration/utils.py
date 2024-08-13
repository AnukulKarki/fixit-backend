from rest_framework_simplejwt.tokens import AccessToken
import rest_framework_simplejwt.exceptions as exceptions
from django.contrib.auth.hashers import make_password
from django.utils.crypto import constant_time_compare

staticsalt = "abeuqiqywj241jsi"

def verify_access_token(token):
    if not token:
        return False, None
    try:
        access_token = AccessToken(token)
        
        access_token.verify()
        payload_data = access_token.payload
        return True, payload_data
    except Exception as e:
        return False, None

def hashPassword(password):
    return make_password(password, staticsalt)