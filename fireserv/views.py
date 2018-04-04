from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import generics
from fireserv.serializers import UserSerializer, AccountSerializer, PhotoSerializer, InquirySerializer, ProductSerializer, ProductImageSerializer
from fireserv.serializers import AgentSerializer, OrderSerializer, ArticleSerializer, OrderProductsSerializer
from fireserv.models import Account, Photo, Inquiry, Product, ProductImage, Agent, Order, Article, OrderProducts
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
import os


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
        account_data['phone'] = data['phone']
        account_data['username'] = data['phone']
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
        return Response({'token': token.key, 'role': role, 'pk': pk}, status=200)

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class CreatePhoto(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            print('photo serializer is VALID!...')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('the following is data errors: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhotoList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoListById(PhotoList):
    def list(self, request, inq_id):
        print('PhotoListById inq_id: ', inq_id)

        photolist = list(Photo.objects.filter(inquiry_id=inq_id).values())
        return Response(photolist, status=200)


class InquiryList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        print ('request.data: ', request.data)
        if serializer.is_valid():
            print('inquiry create request is VALID...')
            instance = serializer.save()
            return Response(instance.id, status=status.HTTP_201_CREATED)
        print('the following is data errors: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InquiryListForUser(InquiryList):
    def list(self, request, acc_id):
        print("data: ", request.body)
        print('acc_id: ', acc_id)

        inquiries = list(Inquiry.objects.filter(account_id=acc_id).values())
        return Response(inquiries, status=200)

class InquiryListUnresolved(InquiryList):
    def list(self, request):
        inquiries = list(Inquiry.objects.filter(status=False).values())
        return Response(inquiries, status=200)


class InquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class AccidByUser(AccountList):
    def list(self, request, user_id):
        acc_id = Account.objects.filter(user=User(id=user_id)).values_list('id', flat=True)[0]
        return Response(acc_id, status=200)

class ProductList(generics.ListCreateAPIView):
    authentication_classes = []

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductImageList(generics.ListCreateAPIView):
    authentication_classes = []

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def post(self, request):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            print('product image serializer is VALID!...')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('the following is data errors for product image: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductImageByProduct(ProductImageList):
    def list(self, request, product_id):
        imageList = ProductImage.objects.filter(product_id=product_id).values()
        return Response(imageList, status=200)

class AgentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class AgentDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class AgentListByAccount(AgentList):
    def list(self, request, acct_id):
        agentList = Agent.objects.filter(acct_id=acct_id).values()
        return Response(agentList, status=200)

@csrf_exempt
@api_view(['POST'])
def hasFirecode(request):
    print('request: ', request)
    print('fire_code: ', request.data)
    code = list(Agent.objects.filter(fire_code=request.data).values())
    print('code: ', code)
    if (len(code) > 0):
        return Response(code[0], status=200)
    else:
        return Response('cannot find matched fire code', status=400)

class OrderList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderProductsList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = OrderProducts.objects.all()
    serializer_class = OrderProductsSerializer

class OrderProductsDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = OrderProducts.objects.all()
    serializer_class = OrderProductsSerializer

class OrderListByAccount(OrderList):
    def list(self, request, acct_id):
        orderList = Order.objects.filter(acct_id=acct_id).values()
        return Response(orderList, status=200)

class OrderProductsListByOrder(OrderProductsList):
    def list(self, request, order_id):
        resultList = OrderProducts.objects.filter(order=Order(id=order_id)).values()
        return Response(resultList, status=200)

class ArticleList(generics.ListCreateAPIView):
    authentication_classes = []

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
