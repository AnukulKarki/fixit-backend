from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import verify_access_token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import BrandItemModelSerializer, BrandModelSerializer
from .models import Brand, BrandItem


# Create your views here.


class BrandPostView(APIView):
    def post(self,request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                serializer = BrandModelSerializer(data = request.data)
                if serializer.is_valid():
                    title = request.data.get("title")
                    userImage = request.data.get("image")
                    Brand.objects.create(title = title, image = userImage)
                    return Response({'msg':'Brand Added Successfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'msg':'Only Valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)           

        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)
    
class BrandItemPostView(APIView):
    def post(self,request):
        token = request.COOKIES.get("token", None)
        verification, payload = verify_access_token(token) 
        if verification:
            if payload['role'].lower() == "admin":
                serializer = BrandItemModelSerializer(data = request.data)
                if serializer.is_valid():
                    brand = serializer.data.get("brand")
                    name = serializer.data.get("name")
                    price = serializer.data.get("price")
                    image = request.data.get("image")
                    BrandItem.objects.create(brand_id = brand, name = name, price = price,image = image)
                    return Response({'msg':'Brand Added Successfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'msg':'Only Valid to worker'}, status=status.HTTP_401_UNAUTHORIZED)           

        return Response({'msg':'Login First'}, status=status.HTTP_401_UNAUTHORIZED)

class BrandList(APIView):
    def get(self, request):
        brandData = Brand.objects.all()
        serializer = BrandModelSerializer(brandData, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BrandItemList(APIView):
    def get(self, request):
        brandData = BrandItem.objects.all()
        serializer = BrandItemModelSerializer(brandData, many = True, context={"request":self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class BrandItemListDetail(APIView):
    def get(self, request, *args, **kwargs):
        brandData = BrandItem.objects.filter(brand_id = kwargs['id'])
        serializer = BrandItemModelSerializer(brandData, many = True, context={"request":self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class BrandItemDelete(APIView):
    def get(self, request, *args, **kwargs):
        BrandItem.objects.filter(id = kwargs['id']).delete()
        return Response({'msg':'Delete Successful'}, status=status.HTTP_200_OK)

class BrandEdit(APIView):
    def post(self, request, *args, **kwargs):
        brandObj = Brand.objects.get(id = kwargs['id'])
        serializer = BrandModelSerializer(data = request.data)
        if serializer.is_valid():
            brandObj.title = request.data.get('title')
            image = request.FILES.get('image')
            if image:
                brandObj.image = image
            brandObj.save()
            return Response({'msg':'Brand Updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class BrandDelete(APIView):
    def get(self, request, *args, **kwargs):
        Brand.objects.filter(id = kwargs['id']).delete()
        return Response({'msg':'Delete Successful'}, status=status.HTTP_200_OK)