
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from fireserv import views as fireviews
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path('users/', fireviews.UserList.as_view()),
    path('users/<int:pk>', fireviews.UserDetail.as_view()),
    #path('accounts/', fireviews.AccountList.as_view()),
    path('create_account/', fireviews.create_account),
    path('accounts/<int:pk>', fireviews.AccountDetail.as_view()),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('protected_auth/', fireviews.protected_auth),
]
