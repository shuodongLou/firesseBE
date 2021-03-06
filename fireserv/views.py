from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
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
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from requests import get
import pytz
import string
import os
import requests
import hashlib
import socket
import random


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
    #print("debug - data: \n", data)
    user_serializer = UserSerializer(data=data)
    #Once we got the username generated, proceed to create the user and GET
    #the user.id.
    if user_serializer.is_valid():
        print("passed user validation")
        print('data after validation: ', data)
        user_serializer.save()
        #now we have our new user created, go ahead to create related account
        account_data = {}
        account_data['user'] = user_serializer.instance.id
        account_data['role'] = data['role']
        account_data['phone'] = data['phone']
        account_data['username'] = data['phone']
        account_data['rec_code'] = data['code']
        account_data['fire_code'] = data['f_code']
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
        #print('auth request body: ', request.body)
        response = super(CustomObtainToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        #print('token: ', token)
        #print('user id : ', token.user_id)
        role = Account.objects.filter(user_id=token.user_id).values_list('role', flat=True)[0]
        pk = Account.objects.filter(user_id=token.user_id).values_list('id', flat=True)[0]
        return Response({'token': token.key, 'role': role, 'pk': pk}, status=200)

@csrf_exempt
@api_view(['GET'])
def logout_user(request):
    #print('user logged in: ', request.user)
    #print('auth_token b: ', request.user.auth_token)
    request.user.auth_token.delete()
    return Response('user logged out off server successfully', status=200)

@csrf_exempt
@api_view(['POST'])
def change_password(request):

    #print('it is a POST request: ', request.data)
    #get user first
    users = User.objects.filter(username=request.data['username'])
    if (len(users) == 0):
        return Response('user not found!', status=400)
    user = users[0]
    #print('the requested user is: ', user)
    user.set_password(request.data['password'])
    user.save()
    return Response('password changed successfully', status=200)


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
        #print ('request.data: ', request.data)
        if serializer.is_valid():
            print('inquiry create request is VALID...')
            instance = serializer.save()
            return Response(instance.id, status=status.HTTP_201_CREATED)
        print('the following is data errors: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InquiryListForUser(InquiryList):
    def list(self, request, acc_id):
        #print("user: ", request.user)
        #print('acc_id: ', acc_id)

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
    authentication_classes = []
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
    authentication_classes = []

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
@api_view(['GET', 'POST'])
@permission_classes([])
@authentication_classes([])
def hasFirecode(request):
    #print('request: ', request)
    #print('fire_code: ', request.data)
    code = list(Agent.objects.filter(fire_code=request.data).values())
    #print('code: ', code)
    if (len(code) > 0):
        return Response(code[0], status=200)
    else:
        return Response('cannot find matched fire code', status=400)

#Generate nounce_str randomly with ASCII letters and digits
def randomGen(size):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


@csrf_exempt
@api_view(['POST'])
def wechatPay(request):
    xml_con = request.data['xml_con']
    url = request.data['url']
    print('xml received: ', xml_con)
    xml2 = ""
    xml2 += "<xml>"
    xml2 += "<appid><![CDATA[wxb401889e868d284c]]></appid>"
    xml2 += "<body><![CDATA[CHELCI燃典护肤-滋养面膜]]></body>"
    xml2 += "<mch_id><![CDATA[1509865351]]></mch_id>"
    xml2 += "<nonce_str><![CDATA[5K8264ILTKCH16CQ2502SI8ZNMTM67VS]]></nonce_str>"
    xml2 += "<notify_url><![CDATA[https://www.chelci.cn]]></notify_url>"
    xml2 += '<scene_info><![CDATA[{"h5_info": {"type":"Wap","wap_url": "https://www.chelci.cn","wap_name": "燃典护肤"}}]]></scene_info>'
    xml2 += "<out_trade_no><![CDATA[20180722151946]]></out_trade_no>"
    xml2 += "<spbill_create_ip><![CDATA[115.171.21.229]]></spbill_create_ip>"
    xml2 += "<total_fee><![CDATA[2]]></total_fee>"
    xml2 += "<trade_type><![CDATA[MWEB]]></trade_type>"
    xml2 += "<sign>857FB4B57B52BAD06EADF53F2CAE0DD1</sign>"
    xml2 += "</xml>"
    #print('xml generated: ', xml2)

    #Generate random value for nounce_str
    nonce_str = randomGen(32)
    print('nonce_str:', nonce_str)

    #get external ip cus_address
    #ex_ip = get('https://api.ipify.org').text
    #print('ip2: ', ex_ip)

    #Constructing long string to be signed on
    lstr = 'appid=' + xml_con['appid'] + '&'
    lstr += 'body=' + xml_con['body'] + '&'
    lstr += 'mch_id=' + xml_con['mch_id'] + '&'
    lstr += 'nonce_str=' + nonce_str + '&'
    lstr += 'notify_url=' + xml_con['notify_url'] + '&'
    lstr += 'out_trade_no=' + xml_con['out_trade_no'] + '&'
    lstr += 'scene_info=' + xml_con['scene_info'] + '&'
    lstr += 'spbill_create_ip=' + xml_con['spbill_create_ip'] + '&'
    lstr += 'total_fee=2&'
    lstr += 'trade_type=' + xml_con['trade_type'] + '&'
    lstr += 'key=' + xml_con['key']

    print(lstr)
    sign = hashlib.md5(lstr.encode('utf-8')).hexdigest().upper()
    print(sign)



    #Constructing XML format
    fmt1 = "<"
    fmt2 = "><![CDATA["
    fmt3 = "]]></"
    fmt4 = ">"
    xml = '<xml>'
    xml += fmt1 + 'appid' + fmt2 + xml_con['appid'] + fmt3 + 'appid' + fmt4
    xml += fmt1 + 'body' + fmt2 + xml_con['body'] + fmt3 + 'body' + fmt4
    xml += fmt1 + 'mch_id' + fmt2 + xml_con['mch_id'] + fmt3 + 'mch_id' + fmt4
    xml += fmt1 + 'nonce_str' + fmt2 + nonce_str + fmt3 + 'nonce_str' + fmt4
    xml += fmt1 + 'notify_url' + fmt2 + xml_con['notify_url'] + fmt3 + 'notify_url' + fmt4
    xml += fmt1 + 'out_trade_no' + fmt2 + xml_con['out_trade_no'] + fmt3 + 'out_trade_no' + fmt4
    xml += fmt1 + 'scene_info' + fmt2 + xml_con['scene_info'] + fmt3 + 'scene_info' + fmt4
    xml += fmt1 + 'spbill_create_ip' + fmt2 + xml_con['spbill_create_ip'] + fmt3 + 'spbill_create_ip' + fmt4
    xml += fmt1 + 'total_fee' + fmt2 + '2' + fmt3 + 'total_fee' + fmt4
    xml += fmt1 + 'trade_type' + fmt2 + xml_con['trade_type'] + fmt3 + 'trade_type' + fmt4
    xml += fmt1 + 'sign' + fmt2 + sign + fmt3 + 'sign' + fmt4
    xml += '</xml>'

    print(xml)

    headers = {'Content-Type': 'text/xml: charset:"UTF-8"'}
    response = requests.post(url, data=xml.encode('utf-8'), headers=headers).text
    print('response: ', u''.join(response))
    if ('SUCCESS' in response):
        return Response(response, status=200)
    else:
        return Response('WechatPay urnified api call failed!', status=500)

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

class RewardsByCode(OrderList):
    def post(self, request):
        now = timezone.now()
        year = now.year
        month = now.month
        day = now.day
        #print('now: ', timezone.now(), year, month, day)
        m_start_time = datetime(year, month, 1, 0, 0, 0)
        m_end_time = datetime(year, month, 31, 23, 59, 59)
        #print('start_time: ', m_start_time)
        #print('end_time: ', m_end_time)

        rewards = Order.objects.filter(fire_code=request.data, time_created__gte=m_start_time, time_created__lte=m_end_time).aggregate(Sum('final_payment'))
        #print('Rewards result: ', rewards)
        return Response(rewards, status=200)

class ArticleList(generics.ListCreateAPIView):
    authentication_classes = []

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
