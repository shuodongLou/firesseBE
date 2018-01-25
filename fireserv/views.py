from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
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
from rest_framework import permissions
import string


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

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
        account_data['role'] = data['role']
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

class CustomObtainToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print('auth request body: ', request.body)
        response = super(CustomObtainToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        print('token: ', token)
        print('user id : ', token.user_id)
        role = Account.objects.filter(user_id=token.user_id).values_list('role', flat=True)[0]
        pk = Account.objects.filter(user_id=token.user_id).values_list('id', flat=True)[0]
        return Response({'token': token.key, 'role': role, 'pk': pk})

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
