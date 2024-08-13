from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializer import UserModelSerializer, UserLoginSerializer, UserModelDataSerializer, ValidationCodeModelSerializer
from .models import  User, VerificationCode
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import verify_access_token, hashPassword 
from blacklist.models import Blacklist
from .emails import sendVerificationEmail
from datetime import datetime, timedelta
from gighire.models import GigProposal, Rating
from proposal.models import Proposal
# Create your views here.

class RegistrationUser(CreateAPIView):
    def post(self, request):
        serializer = UserModelSerializer(data = request.data)
        if serializer.is_valid():
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = hashPassword(request.data.get('password'))
            phone = request.data.get('phone')
            age = request.data.get('age')
            district = request.data.get('district')
            city = request.data.get('city')
            street_name = request.data.get('street_name')
            role = request.data.get('role')
            image = request.FILES.get('image')
            profileImg = request.FILES.get('profileImg')
            citizenship_no = request.data.get('citizenship_no')
            category = request.data.get('category')
            User.objects.create(firstname=firstname, lastname=lastname, email=email, password=password, phone=phone, age=age, district=district, city=city, street_name=street_name, role=role, image=image, profileImg=profileImg, citizenship_no=citizenship_no, category_id=category)
            data = sendVerificationEmail(request.data['email'])
            if data:
                return Response({'msg':'registered successfully not verified'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class loginUser(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            userEmail = request.data.get('email')
            userPassword = hashPassword(request.data.get('password'))
            print(userEmail, userPassword)
            try:

                user = User.objects.get(email = userEmail, password =userPassword)
                if len(Blacklist.objects.filter(user_id = user.id)) > 0:
                    return Response({'msg':'User is blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
                if user.codeVerified == False:
                    data = sendVerificationEmail(request.data['email'])
                    return Response({'msg':'Email not verified', 'email':user.email}, status=status.HTTP_403_FORBIDDEN)
            except:
                
                user = None

            if user:
                role = ""
                refresh = RefreshToken.for_user(user=user)
                if user.role.lower() == "client":
                    refresh["role"]="client"
                    role = "client"
                elif user.role.lower() == "worker":
                    refresh['role'] = "worker"
                    role = "worker"
                else:
                    refresh['role'] = "admin"
                    role = "admin"
                access_token = str(refresh.access_token)
                response= Response({'msg':'Login Successful','token':access_token, 'role':role}, status=status.HTTP_200_OK)
                response.set_cookie(key='token', value=access_token, secure=True, httponly=True, samesite="None")
                return response
            else:
                return Response({'msg':'Invalid Id or password'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class profileView(APIView):
    def get(self,request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            user = User.objects.get(id=payload['user_id'])
            serializer = UserModelDataSerializer(user, context = {"request":self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     worker = Worker.objects.get(worker_id=payload['user_id'])
            #     serializer = WorkerModelSerializer(worker, context = {"request":self.request})
                # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class profileEdit(APIView):
    def post(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            user = User.objects.filter(id=payload['user_id'])
            userObj = User.objects.get(id=payload['user_id'])
            serializer = UserModelDataSerializer( data=request.data, partial=True)
            if serializer.is_valid():
                firstname = request.data.get('firstname')
                lastname = request.data.get('lastname')
                age = request.data.get('age')
                city = request.data.get('city')
                district = request.data.get('district')
                street_address = request.data.get('street_name')
                image = request.FILES.get('image')
                user.update(firstname=firstname, lastname=lastname, age=age, city=city, district=district, street_name=street_address)
                if image:
                    userObj.profileImg = image
                    userObj.save()
                return Response({'msg':'Updated Successfully'}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordChange(APIView):
    def post(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            
            password = hashPassword(request.data.get('password'))
            newpassword = hashPassword(request.data.get('newpassword'))
            user = User.objects.filter(id=payload['user_id'], password = password)
            if len(user) == 0:
                return Response({'msg':'Invalid Password'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user.update(password = newpassword)
            return Response({'msg':'Password Updated Successfully'}, status=status.HTTP_200_OK)
            
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    


class LogoutView(APIView):
    def get(self, request):
        response = Response({"msg":"Log out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('token',  samesite="None")
        return response
    
class UserCheck(APIView):
    def get(self, request): 
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                return Response({"role":"client"}, status=status.HTTP_200_OK)
            elif payload['role'].lower() == "worker":
                return Response({"role":"worker"}, status=status.HTTP_200_OK)
            elif payload['role'].lower() == "admin":
                return Response({'role':'admin'},status=status.HTTP_200_OK)
            return Response({"msg":"Un-authorized user"}, status=status.HTTP_401_UNAUTHORIZED) 
        return Response({"msg":"Login first"}, status=status.HTTP_401_UNAUTHORIZED)

class userProfileId(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            user = User.objects.filter(id=kwargs['id'])
            serializer = UserModelDataSerializer(user,many= True,context = {"request":self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class workerList(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                workerData_a = User.objects.filter(role = "worker")
                workerData = []
                for data in workerData_a:
                    if len(Blacklist.objects.filter(user_id = data.id)) == 0:
                        workerData.append((data))

                serializer = UserModelDataSerializer(workerData, many = True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only Valid to client'}, status=status.HTTP_401_UNAUTHORIZED)           
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class ClientList(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                workerData_a = User.objects.filter(role = "client")
                workerData = []
                for data in workerData_a:
                    if len(Blacklist.objects.filter(user_id = data.id)) == 0:
                        workerData.append((data))

                serializer = UserModelDataSerializer(workerData, many = True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only Valid to client'}, status=status.HTTP_401_UNAUTHORIZED)           
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
#client details
class ClientDetailProfile(APIView):
    def get(self, request, *args, **kwargs):
        user = kwargs['id']
        ProposalObj =  Proposal.objects.filter( job__user_id = user, status="payed").select_related('job')
        GigProposalObj = GigProposal.objects.filter(user_id = user, status="payed")
        completedJobAmount = len(ProposalObj) + len(GigProposalObj)
        amountSpent = 0
        for data in ProposalObj:
            amountSpent += data.amountPayed
        for data in GigProposalObj:
            amountSpent += data.payamount
        GigProposalObjData = GigProposal.objects.filter(user_id = user)
        requestProposal = len(GigProposalObjData)
        return Response({'workcompleted':completedJobAmount, 'amountSpent':amountSpent, 'requestProposal':requestProposal}, status=status.HTTP_200_OK)
    
class WorkerDetailProfile(APIView):
    def get(self, request, *args, **kwargs):
        user = kwargs['id']
        ProposalObj =  Proposal.objects.filter( worker_id = user, status="payed")
        GigProposalObj = GigProposal.objects.filter(worker_id = user, status="payed")
        completedJobAmount = len(ProposalObj) + len(GigProposalObj)
        amountEarned = 0
        for data in ProposalObj:
            amountEarned += data.amountPayed
        for data in GigProposalObj:
            amountEarned += data.payamount
        GigProposalObjData = Proposal.objects.filter(worker_id = user)
        requestProposal = len(GigProposalObjData)
        return Response({'workcompleted':completedJobAmount, 'amountEarned':amountEarned, 'proposal':requestProposal}, status=status.HTTP_200_OK)
#This is for worker profile    
class PersonalWorkerDetailProfile(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            user = payload['user_id']
            ProposalObj =  Proposal.objects.filter( worker_id = user, status="payed")
            GigProposalObj = GigProposal.objects.filter(worker_id = user, status="payed")
            completedJobAmount = len(ProposalObj) + len(GigProposalObj)
            amountEarned = 0
            for data in ProposalObj:
                amountEarned += data.amountPayed
            for data in GigProposalObj:
                amountEarned += data.payamount
            GigProposalObjData = Proposal.objects.filter(worker_id = user)
            requestProposal = len(GigProposalObjData)
            return Response({'workcompleted':completedJobAmount, 'amountEarned':amountEarned, 'proposal':requestProposal}, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class CodeVerification(APIView):
    def post(self, request):
        serializer = ValidationCodeModelSerializer(data = request.data)
        if serializer.is_valid():
            codeData = request.data.get('code')
            email = request.data['email']
            
            user = User.objects.filter(email = email)
            if len(user) == 0:
                return Response({'msg':'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
            verificationCode = VerificationCode.objects.filter(user_id = user[0].id, code = codeData)

            if len(verificationCode) == 0:
                return Response({'msg':'Invalid Code'}, status=status.HTTP_400_BAD_REQUEST)
            
            if verificationCode[0].code == codeData:
                if verificationCode[0].expired.replace(tzinfo=None) < datetime.now():
                    return Response({'msg':'Code Expired'}, status=status.HTTP_400_BAD_REQUEST)
                user[0].codeVerified = True
                user[0].save()
                userObj = User.objects.get(email = email)
                now = datetime.now()
                five_minutes_later = now + timedelta(minutes=5)
                # date_time_obj = datetime.strptime('2024-04-18 11:19:01.695658', '%Y-%m-%d %H:%M:%S.%f')

                # Convert datetime object to string without fractional seconds
                date_time_str = five_minutes_later.strftime('%Y-%m-%d %H:%M:%S')
                refresh = RefreshToken.for_user(user=userObj)
                refresh['time'] = str(date_time_str)
                access_token = str(refresh.access_token)

                return Response({'msg':'Code Verified', 'token':access_token}, status=status.HTTP_200_OK)
            return Response({'msg':'Invalid Code'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResendCode(APIView):
    def post(self, request):
        email = request.data['email']
        data = sendVerificationEmail(email)
        if data:

            return Response({'msg':'Code Sent'}, status=status.HTTP_200_OK)
        return Response({'msg':'Code not Sent'}, status=status.HTTP_400_BAD_REQUEST)

class verifyUser(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                user = User.objects.filter(id = kwargs['id'])
                if len(user)== 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                user.update(isKycVerified = True)
                return Response({'msg':'User Verified'}, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePassword(APIView):
    def post(self, request):
        token = request.data.get('token')
        print(token)
        verification, payload = verify_access_token(token)

        if verification:
            userId = payload['user_id']
            expiry = payload['time']
            password = hashPassword(request.data.get('password'))
            date_format = '%Y-%m-%d %H:%M:%S'
            # Convert the string to a datetime object
            date_time_obj = datetime.strptime(expiry, date_format)
            if datetime.now() < date_time_obj:
                userobj = User.objects.filter(id = userId)
                userobj.update(password = password)
                return Response({'msg':'password Updated successfully'}, status=status.HTTP_200_OK)

            return Response({'msg':'time expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'not verified'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileEditAdmin(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                user = User.objects.filter(id = kwargs['id'])
                serializer = UserModelDataSerializer( data=request.data, partial=True)
                if serializer.is_valid():
                    firstname = request.data.get('firstname')
                    lastname = request.data.get('lastname')
                    age = request.data.get('age')
                    city = request.data.get('city')
                    district = request.data.get('district')
                    street_address = request.data.get('street_name')
                    user.update(firstname=firstname, lastname=lastname, age=age, city=city, district=district, street_name=street_address)
                    return Response({'msg':'Updated Successfully'}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)           
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class AdminUserUpdate(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            if payload['role'].lower() == "admin":
                user = User.objects.filter(id = kwargs['id'])
                serializer = UserModelDataSerializer( data=request.data, partial=True)
                if serializer.is_valid():
                    firstname = request.data.get('firstname')
                    lastname = request.data.get('lastname')
                    age = request.data.get('age')
                    city = request.data.get('city')
                    district = request.data.get('district')
                    street_address = request.data.get('street_name')
                    phone = request.data.get('phone')
                    user.update(firstname=firstname, lastname=lastname, age=age, city=city, district=district, street_name=street_address, phone=phone)
                    return Response({'msg':'Updated Successfully'}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
        
class passwordHash(APIView):
    def post(self, request):
        password = "Anukul"
        hashedPassword = hashPassword(password)
        return Response({'password':hashedPassword}, status=status.HTTP_200_OK)


