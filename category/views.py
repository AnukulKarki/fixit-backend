from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from .serializer import  CategoryModelSerializer
from .models import Category
# Create your views here.

class CategoryListView(APIView):
    def get(self, request):
        categoryObj = Category.objects.all()
        serializer = CategoryModelSerializer(categoryObj, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryAddView(APIView):
    def post(self, request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                seriaizer = CategoryModelSerializer(data = request.data)
                if seriaizer.is_valid():
                    name = request.data.get('name')
                    Category.objects.create(name = name)
                    return Response({'msg':'Category Added Successfully'}, status=status.HTTP_201_CREATED)
                return Response(seriaizer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'login '}, status=status.HTTP_401_UNAUTHORIZED)
    
class CategoryAdd(APIView):
    def post(self, request):
        seriaizer = CategoryModelSerializer(data = request.data)
        if seriaizer.is_valid():
            name = request.data.get('name')
            Category.objects.create(name = name)
            return Response({'msg':'Category Added Successfully'}, status=status.HTTP_201_CREATED)
        return Response(seriaizer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryEditView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                seriaizer = CategoryModelSerializer(data = request.data)
                if seriaizer.is_valid():
                    name = request.data.get('name')
                    categoryObj = Category.objects.filter(id = kwargs['id'])
                    if len(categoryObj) == 0:
                        return Response({'msg':'Category Not Found'}, status=status.HTTP_404_NOT_FOUND)
                    categoryObj.update(name = name)
                    return Response({'msg':'Update Successfully'}, status=status.HTTP_200_OK)
                return Response(seriaizer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'login First'}, status=status.HTTP_401_UNAUTHORIZED)

# class CategoryDeleteView(APIView):
#     def get(self, request, *args, **kwargs):
#         token = request.COOKIES.get("token", None)
#         verification, payload = verify_access_token(token) 
#         if verification:
#             if payload['role'].lower() == "admin":
#                 categoryObj = Category.objects.filter(kwargs['id'])
#                 if len(categoryObj) == 0:
#                     return Response({'msg':'Category Not Found'}, status=status.HTTP_404_NOT_FOUND)
#                 categoryObj.delete()
#                 return Response({'msg':'Delete Successful'}, status=status.HTTP_200_OK)
#             return Response({'msg':'Only Valid to admin'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response({'msg':'login First'}, status=status.HTTP_401_UNAUTHORIZED)
    

class CategoryDeleteView(APIView):
    def get(self, request, *args, **kwargs):
        
        categoryObj = Category.objects.filter(id = kwargs['id'])
        if len(categoryObj) == 0:
            return Response({'msg':'Category Not Found'}, status=status.HTTP_404_NOT_FOUND)
        categoryObj.delete()
        return Response({'msg':'Delete Successful'}, status=status.HTTP_200_OK)
