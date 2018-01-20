from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics
from fireserv.serializers import UserSerializer, AccountSerializer
from fireserv.models import Account
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
import string
from random import *


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    def show_request(self):
        print("HTTP method:")
        print(self.request.method)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@csrf_exempt
@api_view(['POST'])
def create_account(request):
    data = request.data
    print("debug - data: \n", data)
    user_serializer = UserSerializer(data=data)
    #Once we got the username generated, proceed to create the user and GET
    #the user.id.
    if user_serializer.is_valid():
        print("passed user validation")
        user_serializer.save()
        #now we have our new user created, go ahead to create related account
        account_data = {}
        account_data['user'] = user_serializer.instance.id
        #account_data['phonenum'] = data['phonenum']
        account_serializer = AccountSerializer(data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return Response(account_serializer.data, status=201)
        else:
            print(account_serializer.errors)
            return JsonResponse(account_serializer.errors, status=400)
    else:
        print(user_serializer.errors)
        return JsonResponse(user_serializer.errors, status=400)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def protected_auth(request):
    print("in protected")
    print(request.method)
    if request.auth is not None:
        print(request.auth)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
