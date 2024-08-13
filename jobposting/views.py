from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from .serializer import  JobRequirementAddModelSerializer, JobRequirementModelSerializer, JobRequirementModelSerializerPOST
from .models import JobRequirement
from proposal.models import Proposal


#Job requirement Posting
class JobRequirementPostView(APIView):
    def post(self,request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                serializer = JobRequirementAddModelSerializer(data=request.data)
                if serializer.is_valid():
                    title = request.data.get('title')
                    description = request.data.get('description')
                    budget = request.data.get('budget')
                    isFeatured = request.data.get('isFeatured')
                    latitude = request.data.get('latitude')
                    longitude = request.data.get('longitude')
                    location = request.data.get('location')
                    image = request.data.get('image')
                    category = request.data.get('category')

                    dataCreation = JobRequirement.objects.create(title = title, description = description, budget = budget, isFeatured = isFeatured, latitude = latitude, longitude = longitude, location = location, image = image, category_id = category, user_id = payload['user_id'])
                    return Response({'msg':'Data Entered Successfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'msg':'Only Valid to user'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)


 

import math
#All Job Requirement Post
class JobRequirementListView(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            #no need to check user as it displays all the data
            JobRequirementList  = JobRequirement.objects.filter(jobStatus = 'inprogress').order_by('-created_at')

            serializer = JobRequirementModelSerializer(JobRequirementList, many = True, context = {"request":self.request} )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class NearJobRequirementListView(APIView):
    def post(self, request):
        token = request.COOKIES.get("token")
        verification, payload = verify_access_token(token)
        if verification:
            lati1 = float(request.data.get("latitude"))
            long1 = float(request.data.get("longitude"))
            jobreqlist = JobRequirement.objects.filter(jobStatus = 'inprogress').order_by('-created_at')
            jobData = []
            for data in jobreqlist:
                lati2 = float(data.latitude)
                long2 = float(data.longitude)

                lon1, lat1, lon2, lat2 = map(math.radians, [long1, lati1, long2, lati2])

                # Haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
                c = 2 * math.asin(math.sqrt(a))

                r = 6371

                # Calculate the result
                
                distance = c * r
                # listdata[data.location] = distance
                # cords[data.location] = [lat2,lon2, data.latitude, data.longitude]
                # return Response({"distance":listdata,'coords':cords, "latitude1":lat1, "longitude1":lon1}, status=status.HTTP_200_OK)
                if distance < 20:
                    
                    jobData.append(data)
                serailizer = JobRequirementModelSerializerPOST(jobData, many=True,context = {"request":self.request})
            return Response(serailizer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

    
#Job Requirement Details of particular loged in user only
class JobRequirementListViewUser(APIView):
    def get(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                
                JobRequirementList  = JobRequirement.objects.filter(user_id = payload['user_id']).order_by('-created_at')
                serializer = JobRequirementModelSerializer(JobRequirementList, many = True, context = {"request":self.request} )
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'msg':'Only Valid to user'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
    

#Job Requirement Edit 
class JobRequirementEditView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                JobRequirementObj = JobRequirement.objects.filter(id = kwargs['id'], user_id = payload['user_id'])
                if len(JobRequirementObj) == 0:
                    return Response({'msg':'Job Requirement Not Found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = JobRequirementAddModelSerializer(data=request.data)
                if serializer.is_valid():
                    title = request.data.get('title')
                    description = request.data.get('description')
                    budget = request.data.get('budget')
                    isFeatured = request.data.get('isFeatured')
                    latitude = request.data.get('latitude')
                    longitude = request.data.get('longitude')
                    location = request.data.get('location')
                    image = request.data.get('image')
                    category = request.data.get('category')
                    JobRequirementObj.update(title = title, description = description, budget = budget, isFeatured = isFeatured, latitude = latitude, longitude = longitude, location = location, image = image, category_id = category, user_id = payload['user_id'])

                    return Response({"msg":"Job Requirement Edit Successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only valid to User'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg':'Login First'}, status=status.HTTP_403_FORBIDDEN)
    
#Job Requirmeent Delete
class JobRequirementDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                try:
                    JobRequirement.objects.get(id = kwargs['id'] , user_id = payload['user_id'] ).delete()
                    return Response({'msg':'Delete Successful'}, status=status.HTTP_200_OK)
                except:
                    return Response({'msg':'Job Req Not found'}, status=status.HTTP_404_NOT_FOUND)
    
            return Response({'msg':'Only Valid to User'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'msg':'Login First'}, status=status.HTTP_403_FORBIDDEN)
    

    
#Job Requirement Detail
class JobRequirementDetailView(APIView):
    def get(self, request, *args, **kwargs):
        
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            try:

                JobRequirementList  = JobRequirement.objects.get(id = kwargs['id'])
                serializer = JobRequirementModelSerializer(JobRequirementList, context = {"request":self.request} )

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Job Requirement Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'Login First'}, status=status.HTTP_403_FORBIDDEN)
    
class JobRequirementUserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "client":
                try:
                    JobRequirementList  = JobRequirement.objects.get(id = kwargs['id'], user_id = payload['user_id'])
                    serializer = JobRequirementModelSerializer(JobRequirementList,  context = {"request":self.request} )
            
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:

                    return Response({'msg':'Job Requirement not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'msg':'Only Valid to User'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'Login First'}, status=status.HTTP_403_FORBIDDEN)

from category.models import Category
class JobFilter(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            category = kwargs['category']
            maxPrice = kwargs['maxprice']
            minPrice = kwargs['minprice']
            print(category)
            print(type(category))
            print(type(maxPrice), type(minPrice))
            print(maxPrice, minPrice)
            print("min price", minPrice)
            print("max price", maxPrice)
            #no need to check user as it displays all the data
            JobRequirementList  = JobRequirement.objects.filter(jobStatus = 'inprogress', category_id = category , budget__gte = minPrice, budget__lte = maxPrice).order_by('-created_at')
            print("length")
            print(len(JobRequirementList))
            serializer = JobRequirementModelSerializer(JobRequirementList, many = True, context = {"request":self.request} )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class ProposalNumber(APIView):
    def get(self, request, *args, **kwargs):
        JobRequirementList  = Proposal.objects.filter(id = kwargs['id'], status = 'inprogress')
        return Response({'number':len(JobRequirementList)}, status=status.HTTP_200_OK)

