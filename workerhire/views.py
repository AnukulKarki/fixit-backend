from django.shortcuts import render
from rest_framework.views import APIView
from proposal.serializer import ProposalApplySerializer, ProposalApplyWorkerSerializer
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from proposal.models import Proposal
from django.utils import timezone
import datetime
from jobposting.models import JobRequirement
from registration.emails import sendConfirmationEmail

# Create your views here.
#hire the worker, by accepting one and rejecting other at once
#have to update the job requirement database that worker have been found.
class WorkerHire(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                proposalId = kwargs['id']
                jobId = kwargs['jobid']
               
                JobRequirementObj = JobRequirement.objects.filter(id =jobId)
                if JobRequirementObj[0].jobStatus.lower() == "inprogress":
                
                    proposalObj = Proposal.objects.filter(id = proposalId)
                    if len(proposalObj) == 0:
                        return Response({'msg':'not found'}, status=status.HTTP_404_NOT_FOUND)
                    if proposalObj[0].job.user_id == payload['user_id']:
                        proposalObj.update(status = "accept", accepted_at = datetime.datetime.now().date())
                        sendConfirmationEmail(proposalObj[0].worker.email, proposalObj[0].job.user.firstname +proposalObj[0].job.user.lastname , proposalObj[0].job.title, proposalObj[0].job.user.phone, proposalObj[0].job.user.email)
                        proposalObjToUpdate = Proposal.objects.exclude(id = proposalId).filter(job_id = jobId) #update reject status except the one that is accepted
                        proposalObjToUpdate.update(status = "rejected")
                        JobRequirement.objects.filter(id = jobId).update(jobStatus= "accepted")
                        return Response({'msg':'Worker Hired Successfully'}, status = status.HTTP_200_OK)
                return Response({'msg':'Worker Already Hired'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'msg':'Only Valid to client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"msg":"Login first"}, status=status.HTTP_401_UNAUTHORIZED)


#Have to create a view to reject the worker.
class WorkerRejectView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                proposalId = kwargs['id']
               
                proposalObj = Proposal.objects.filter(id = proposalId)
                if len(proposalObj) == 0:
                    return Response({'msg':'not found'}, status=status.HTTP_404_NOT_FOUND)
                if proposalObj[0].status == 'applied':
                    if proposalObj[0].job.user_id == payload['user_id']:
                        proposalObj.update(status="rejected")
                        return Response({'msg':'Worker Rejected'}, status = status.HTTP_200_OK)
                    return Response({'msg':'only valid to owner'}, status=status.HTTP_401_UNAUTHORIZED)
                return Response({'msg':'Cannot reject who have not applied'}, status=status.HTTP_401_UNAUTHORIZED)
                
            return Response({'msg':'Only Valid to client'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"msg":"Login first"}, status=status.HTTP_401_UNAUTHORIZED)


