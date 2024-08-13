
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .serializer import GigProposalModelAddSerializer, GigProposalModelSerializer, GigProposalModelPaySerializer, RateModelSerializer, ReportModelSerializer
from .models import GigProposal
import datetime
from .models import Rating, Report
from registration.models import User
from django.db.models import Q
from registration.emails import sendConfirmationEmail

class GigProposalApplyView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                serializer = GigProposalModelAddSerializer(data = request.data)
                userObj = User.objects.filter(id = kwargs['id'])
                if userObj[0].role.lower() != "worker":
                    return Response({'msg':'User is not worker'}, status=status.HTTP_404_NOT_FOUND)
                if serializer.is_valid():
                    title = request.data.get('worktitle')
                    description = request.data.get('workdescription')
                    location = request.data.get('location')
                    latitude = request.data.get('latitude')
                    longitude = request.data.get('longitude')
                    image = request.data.get('image')
                    category = request.data.get('category')
                    GigProposal.objects.create(worker_id = kwargs['id'], user_id = payload['user_id'],category_id = category ,worktitle = title, workdescription = description, location =location, latitude = latitude, longitude = longitude, image = image)
                    return Response({'msg':'Proposal Submit Successfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only valid to client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class GigProposalListview(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        
        if verification:
            if payload['role'].lower() == "worker":
                gigProposalView = GigProposal.objects.filter(worker_id = payload['user_id'], status = "applied")
                
                if len(gigProposalView) == 0:
                    return Response({'msg':'No Request'},status=status.HTTP_404_NOT_FOUND)
                serializer = GigProposalModelSerializer(gigProposalView, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class GigProposalDetailview(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        
        if verification:
            if payload['role'].lower() == "worker":
                gigProposalView = GigProposal.objects.filter(id = kwargs['id'])
                
                if len(gigProposalView) == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer = GigProposalModelSerializer(gigProposalView, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)



class GigProposalAcceptView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker": 
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "applied":
                    sendConfirmationEmail(GigProposalObj[0].user.email, GigProposalObj[0].worker.firstname + GigProposalObj[0].worker.lastname, GigProposalObj[0].worktitle, GigProposalObj[0].worker.phone, GigProposalObj[0].worker.email)
                    GigProposalObj.update(status="accept", acceptedate = datetime.datetime.now().date())
                    return Response({'msg':'Proposal Accepted'}, status=status.HTTP_200_OK)
                return Response({'msg':'cant accept the proposal'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigProposalRejectView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker": 
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "applied":
                    GigProposalObj.update(status="reject")
                return Response({'msg':'Proposal Rejected'}, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class CurrentGigWorkView(APIView):
    def get(self, request,):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker": 
                GigProposalObj = GigProposal.objects.filter(worker_id = payload['user_id'])
                CurrentGigWork = GigProposalObj.exclude(status='cancel').exclude(status='payed').exclude(status='reject').exclude(status='applied')
                serializer = GigProposalModelSerializer(CurrentGigWork, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class CurrentGigWorkClientView(APIView):
    def get(self, request,):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client": 
                GigProposalObj = GigProposal.objects.filter(user_id = payload['user_id'])
                CurrentGigWork = GigProposalObj.exclude(status='cancel').exclude(status='payed').exclude(status='reject').exclude(status='applied')
                serializer = GigProposalModelSerializer(CurrentGigWork, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class GigWorkStartView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker": 
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "accept":
                    GigProposalObj.update(status="started")
                    return Response({'msg':'Work Started', 'job':'Started'}, status=status.HTTP_200_OK)
                if GigProposalObj[0].status.lower() == "started":
                    GigProposalObj.update(status="completed")
                    return Response({'msg':'Work Completed', 'job':'Completed'}, status=status.HTTP_200_OK)
                
                return Response({'msg':'Cannot Start the work'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)


class GigWorkCompleteView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker": 
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "started":
                    GigProposalObj.update(status="completed")
                return Response({'msg':'Work Completed'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigWorkCancelView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
            if len(GigProposalObj) == 0:
                return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
            if GigProposalObj[0].status.lower() == "accept":
                GigProposalObj.update(status="cancel")
            return Response({'msg':'Work cancel','job':'Cancel'}, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class GigWorkPayView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client": 
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "completed":
                    serializer = GigProposalModelPaySerializer(data = request.data)
                    if serializer.is_valid():
                        amount = request.data.get('payamount')
                        method = request.data.get('paymethod')
                        GigProposalObj.update(status="payed", payamount = amount, paymethod = method)

                        return Response({'msg':'Payment Successfull'}, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg':'Cannot Pay'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'msg':'Only valid to Client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class RatingView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            gigJobObj = None
            if payload['role'].lower() == "worker":
                gigJobObj = GigProposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
            else:
                gigJobObj = GigProposal.objects.filter(id = kwargs['id'], user_id = payload['user_id'])
            
            if gigJobObj[0].status.lower() == "payed":
                rateObj = Rating.objects.filter(rateuser_id = payload['user_id'], gigproposal_id = kwargs['id'])
                if len(rateObj) >0:
                    return Response({'msg':'You have already rated the user'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = RateModelSerializer(data = request.data)
                if serializer.is_valid():
                    rate = request.data.get('rate')
                    if payload['role'].lower() == "worker":
                        rateduser = gigJobObj[0].user_id
                        Rating.objects.create(rateuser_id = payload['user_id'], gigproposal_id = kwargs['id'],rateduser_id = rateduser, rate = rate)
                    else:
                        rateduser= gigJobObj[0].worker_id
                        Rating.objects.create(rateuser_id = payload['user_id'], gigproposal_id = kwargs['id'],rateduser_id = rateduser, rate = rate)

                    rateData  = Rating.objects.filter(rateduser_id = rateduser)
                    totalRating = 0
                    for rateObj in rateData:
                        totalRating += rateObj.rate
                    avg = totalRating/len(rateData)
                    User.objects.filter(id =rateduser ).update(rating = avg)

                    return Response({'msg':'Rated Successfully'}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'msg':'Cannot Rate'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigProposalClientRequest(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                GigProposalObj = GigProposal.objects.filter(user_id = payload['user_id'], status = "applied")
                serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class deleteProposal(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                GigProposalObj = GigProposal.objects.filter(id = kwargs['id'], user_id = payload['user_id'])
                if len(GigProposalObj) == 0:
                    return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
                if GigProposalObj[0].status.lower() == "applied":
                    GigProposalObj.delete()
                    return Response({'msg':'Proposal Deleted'}, status=status.HTTP_200_OK)
                return Response({'msg':'Cannot Delete'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only valid to Client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigWorkDetail(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            GigProposalObj = GigProposal.objects.filter(id = kwargs['id'])
            if len(GigProposalObj) == 0:
                return Response({'msg':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigPastWork(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker":
                GigProposalObja = GigProposal.objects.filter(worker_id = payload['user_id'])
                GigProposalObj = GigProposalObja.filter(Q(status="payed") | Q(status="cancel"))
                serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GigPastWorkId(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            workerId = kwargs['id']
            GigProposalObja = GigProposal.objects.filter(worker_id = workerId)
            GigProposalObj = GigProposalObja.filter(status="payed")
            serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)    


class GigPastWorkClient(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                GigProposalObja = GigProposal.objects.filter(user_id = payload['user_id'])
                GigProposalObj = GigProposalObja.filter(Q(status="payed") | Q(status="cancel"))
                serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'Only valid to Worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class GigPastWorkClientId(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            userId = kwargs['id']
            GigProposalObja = GigProposal.objects.filter(user_id = userId)
            GigProposalObj = GigProposalObja.filter(status="payed")
            serializer = GigProposalModelSerializer(GigProposalObj, many = True, context = {'request':self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class ReportWork(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            workId = None
            if payload['role'].lower() == "worker":
                workId  = GigProposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
            else:
                workId  = GigProposal.objects.filter(id = kwargs['id'], user_id = payload['user_id'])
            
            if len(workId) == 0:
                return Response({'msg':'Work Not found'}, status=status.HTTP_404_NOT_FOUND)
            if workId[0].status.lower() == "payed":
                reportObj = Report.objects.filter(reportuser_id = payload['user_id'], gigproposal_id = kwargs['id'])
                if len(reportObj) > 0:
                    return Response({'msg':'Already Reported The user'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = ReportModelSerializer(data = request.data)
                if serializer.is_valid(raise_exception=True):
                    report = request.data.get('report')
                    reporteduser = None
                    if payload['role'].lower() == "worker":
                        reporteduser = workId[0].user_id
                        Report.objects.create(reportuser_id = payload['user_id'], gigproposal_id = kwargs['id'] ,reporteduser_id = reporteduser, report = report)
                    else:
                        reporteduser = workId[0].worker_id
                        Report.objects.create(reportuser_id = payload['user_id'], gigproposal_id = kwargs['id'] ,reporteduser_id = reporteduser, report = report)
                    return Response({'msg':'Reported Successfully'}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Cannot Report'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class ReportList(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            reportObj = Report.objects.filter(reporteduser_id = kwargs['id'])
            serializer = ReportModelSerializer(reportObj, many = True, context = {'request':self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
             