from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from proposal.models import Proposal
from proposal.serializer import ProposalApplyWorkerSerializer
from jobposting.models import JobRequirement
from .serializer import PayModelSerializer
from gighire.models import Rating, Report
from gighire.serializer import RateModelSerializer, ReportModelSerializer
from registration.models import User 
from django.db.models import Q
import json
import requests
from django.shortcuts import redirect
from gighire.models import GigProposal
from django.http import HttpResponseRedirect

class CurrentWorkerWorkView(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker":
                workData = Proposal.objects.filter(worker_id = payload['user_id'])
                workerCurrentData = workData.exclude(status="rejected").exclude(status="payed").exclude(status='cancel').exclude(status='applied')
                serializer = ProposalApplyWorkerSerializer(workerCurrentData, many= True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'only valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class CurrentWorkerClientView(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                jobId = Proposal.objects.filter(job__user_id = payload['user_id']).select_related('job')
                jobIdActive = jobId.exclude(status="rejected").exclude(status="payed").exclude(status = 'cancel').exclude(status = 'applied')
                serializer = ProposalApplyWorkerSerializer(jobIdActive, many= True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'only valid to Client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class CancelCurrentWorkerView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker":
                
                workId  = Proposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
                if len(workId) == 0:
                    return Response({'msg':'Work Not found'})
                if workId[0].status.lower() != "accept":
                    return Response({'msg':'Cannot Cancel the work'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                workId.update(status="cancel")
                JobRequirement.objects.filter(id = workId[0].job_id).update(jobStatus="cancel")
                return Response({'msg':'Job Cancelled Successfully', 'job':'Cancel'}, status=status.HTTP_200_OK)    
            return Response({'msg':'only valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

#Start the work
class startProgress(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker":
                workId  = Proposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
                if len(workId) == 0:
                    return Response({'msg':'Work Not found'})
                if workId[0].status.lower() == "accept":
                    workId.update(status="started")
                    return Response({'msg':'Job Started Successfully','job':'Started'}, status=status.HTTP_200_OK)
                if workId[0].status.lower() == "started":
                    workId.update(status="completed")
                    return Response({'msg':'Job completed Successfully','job':'Completed'}, status=status.HTTP_200_OK) 
                return Response({'msg':'Cannot Start the work'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                   
            return Response({'msg':'only valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

#complete the current work

    

class PayWorkView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                workId  = Proposal.objects.filter(id = kwargs['id'])
                if len(workId) == 0:
                    return Response({'msg':'Work Not found'})
                if workId[0].status.lower() == "completed":
                    #pay The worker using cash
                    serailizer = PayModelSerializer(data = request.data)
                    if serailizer.is_valid():
                        amount = request.data.get('amountPayed')
                        method = request.data.get('paymethod')
                        workId.update(amountPayed = amount, paymethod = method, status = 'payed')
                        JobRequirement.objects.filter(id = workId[0].job_id).update(jobStatus="completed")

                        return Response({'msg':'Amount Payed Successfully'}, status=status.HTTP_200_OK) 
                    return Response(serailizer.errors, status=status.HTTP_200_OK) 
                return Response({'msg':'Work Is not complete yet'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'msg':'only valid to User'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)


class RatingView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            workId = None
            if payload['role'].lower() == "worker":
                workId  = Proposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
            else:
                workId  = Proposal.objects.filter(id = kwargs['id'], job__user_id = payload['user_id']).select_related('job')

            if len(workId) == 0:
                return Response({'msg':'Work Not found'}, status=status.HTTP_404_NOT_FOUND)
            if workId[0].status.lower() == "payed":

                rateObj = Rating.objects.filter(rateuser_id = payload['user_id'], jobproposal_id = workId[0].job_id )
                if len(rateObj) > 0:
                    return Response({'msg':'Already Rated The user'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = RateModelSerializer(data = request.data)
                if serializer.is_valid():
                    rate = request.data.get('rate')
                    rateduser = None
                    if payload['role'].lower() == "worker":
                        rateduser = workId[0].job.user_id
                        Rating.objects.create(rateuser_id = payload['user_id'], jobproposal_id = workId[0].job_id ,rateduser_id = rateduser, rate = rate)
                    else:
                        rateduser = workId[0].worker_id
                        Rating.objects.create(rateuser_id = payload['user_id'], jobproposal_id = workId[0].job_id ,rateduser_id = rateduser, rate = rate)

                    rateData  = Rating.objects.filter(rateduser_id = rateduser)
                    totalRating = 0
                    for rateObj in rateData:
                        totalRating += rateObj.rate
                    avg = totalRating/len(rateData)
                    User.objects.filter(id =rateduser ).update(rating = avg)
                        

                    return Response({'msg':'Rated Successfully'}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            return Response({'msg':'Cannot Rate'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)




class PastWorkViewWorker(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "worker":
                workData = Proposal.objects.filter(worker_id = payload['user_id'])
                workerCurrentData = workData.filter(Q(status="payed") | Q(status="cancel"))
                serializer = ProposalApplyWorkerSerializer(workerCurrentData, many= True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'only valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
#get the details of past worker using the id of the worker from id.
class PastWorkViewWorkerId(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            workerId = kwargs['id']
            workData = Proposal.objects.filter(worker_id = workerId)
            workerCurrentData = workData.filter(status="payed")
            serializer = ProposalApplyWorkerSerializer(workerCurrentData, many= True, context = {"request":self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)


class PastWorkViewClient(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                workData = Proposal.objects.filter(job__user_id = payload['user_id']).select_related('job')
                workerCurrentData = workData.filter(Q(status="payed") | Q(status="cancel"))
                serializer = ProposalApplyWorkerSerializer(workerCurrentData, many= True, context = {"request":self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'msg':'only valid to Client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
#get the details of the past work from client id through email
class PastWorkViewClientId(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            userId = kwargs['id']
            workData = Proposal.objects.filter(job__user_id = userId).select_related('job')
            workerCurrentData = workData.filter(status="payed")
            serializer = ProposalApplyWorkerSerializer(workerCurrentData, many= True, context = {"request":self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class WorkDescriptionView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            workId = Proposal.objects.filter(id = kwargs['id'])
            if len(workId) == 0:
                return Response({'msg':'Work Not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProposalApplyWorkerSerializer(workId, many= True, context = {"request":self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

import random
class KhaltiPayment(APIView):
    def post(self, request, *args, **kwargs):
        khaltiAPI = "https://a.khalti.com/api/v2/epayment/initiate/"
        website_url = "http://localhost:3000/"

        amount = int(request.data.get("amount"))*100
        jobid = request.data.get("jobid")
        jobtype = request.data.get("jobtype")
        key = 0
        name =""
        email = ""
        if jobtype == "requirement":
            key = 1
            jobreqiObj = Proposal.objects.filter(id = jobid)
            userId = jobreqiObj[0].job.user_id
            userObj = User.objects.filter(id = userId)
            if len(userObj) > 0:
                name = userObj[0].firstname
                email = userObj[0].email
        else:
            key = 2
            jobreqiObj = GigProposal.objects.filter(id = jobid)
            userId = jobreqiObj[0].user_id
            userObj = User.objects.filter(id = userId)
            if len(userObj) > 0:
                name = userObj[0].firstname
                email = userObj[0].email

        return_url = "http://localhost:8000/api/work/khalti-verify/"+str(jobid)+"/"+str(key)+"/"
        purchase_order_id = "123456789"
        purchase_name = "test"

        headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455', 
            'Content-Type': 'application/json',
        }

        payload = json.dumps({
            "return_url": return_url,
            "website_url": website_url,
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_name,
            "customer_info":{
                "name": name,
                "email": email,
            }
        })
        
        response = requests.post(khaltiAPI, data = payload, headers = headers)
        
        new_res = json.loads(response.text)
        print(new_res)
        if new_res['payment_url']:
            return Response({'url':new_res['payment_url']}, status=status.HTTP_200_OK)
        
        return Response({'msg':'Failure'}, status=status.HTTP_400_BAD_REQUEST)


class verifyKhalti(APIView):
    def get(self, request, *args, **kwargs):
        jobid = kwargs['id']
        key = kwargs['key']
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
    
        if request.method == 'GET':
            headers = {
                'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
                'Content-Type': 'application/json',
            }
            pidx = request.GET.get('pidx')
            payload = json.dumps({
            'pidx': pidx
            })
            print('payload re hai:: ', payload)
            res = requests.request('POST',url,headers=headers,data=payload)
            new_res = json.loads(res.text)
            print("res", new_res)

            if new_res['status'] == 'Completed':
                amount = new_res['total_amount']/100
                if key == 1:
                    proposalId = Proposal.objects.filter(id = jobid)
                    Proposal.objects.filter(id = jobid).update(status = "payed", amountPayed = amount, paymethod = "khalti")
                    JobRequirement.objects.filter(id = proposalId[0].job_id).update(jobStatus="completed")
                    return HttpResponseRedirect('http://localhost:3000/clientjobpage')

                else:
                    GigProposal.objects.filter(id = jobid).update(status = "payed", payamount = amount, paymethod = "khalti")

                    return HttpResponseRedirect('http://localhost:3000/clientjobpage')
            return Response({'msg':'Payment Not Completed'}, status=status.HTTP_400_BAD_REQUEST)

class ReportWork(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token)
        if verification:
            workId = None
            if payload['role'].lower() == "worker":
                workId  = Proposal.objects.filter(id = kwargs['id'], worker_id = payload['user_id'])
            else:
                workId  = Proposal.objects.filter(id = kwargs['id'], job__user_id = payload['user_id']).select_related('job')
            
            if len(workId) == 0:
                return Response({'msg':'Work Not found'}, status=status.HTTP_404_NOT_FOUND)
            if workId[0].status.lower() == "payed":

                rateObj = Report.objects.filter(reportuser_id = payload['user_id'], jobproposal_id = workId[0].job_id )
                if len(rateObj) > 0:
                    return Response({'msg':'Already Reported The user'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = ReportModelSerializer(data = request.data)
                if serializer.is_valid(raise_exception=True):
                    report = request.data.get('report')
                    reporteduser = None
                    if payload['role'].lower() == "worker":
                        reporteduser = workId[0].job.user_id
                        Report.objects.create(reportuser_id = payload['user_id'], jobproposal_id = workId[0].job_id ,reporteduser_id = reporteduser, report = report)
                    else:
                        reporteduser = workId[0].worker_id
                        Report.objects.create(reportuser_id = payload['user_id'], jobproposal_id = workId[0].job_id ,reporteduser_id = reporteduser, report = report)
                    return Response({'msg':'Reported Successfully'}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Cannot Report'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
            

