
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from fireserv import views as fireviews
from rest_framework.authtoken import views as authviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', fireviews.UserList.as_view()),
    path('users/<int:pk>', fireviews.UserDetail.as_view()),
    path('accounts/', fireviews.AccountList.as_view()),
    path('create_account/', fireviews.create_account),
    path('accounts/<int:pk>', fireviews.AccountDetail.as_view()),
    #path('api-token-auth/', authviews.obtain_auth_token),
    path('custom-token-auth/', fireviews.CustomObtainToken.as_view()),
    path('storeimg/', fireviews.CreatePhoto.as_view()),
    path('inquiries/', fireviews.InquiryList.as_view()),
    path('inquiries/<int:pk>', fireviews.InquiryDetail.as_view()),
    path('inquiriesforuser/<int:acc_id>', fireviews.InquiryListForUser.as_view()),
    path('unresolvedinquiries/', fireviews.InquiryListUnresolved.as_view()),
    path('getphotobyinquiryid/<int:inq_id>', fireviews.PhotoListById.as_view()),
    path('getaccidbyuser/<int:user_id>', fireviews.AccidByUser.as_view()),
    path('products/', fireviews.ProductList.as_view()),
    path('products/<int:pk>', fireviews.ProductDetail.as_view()),
    path('productimages/', fireviews.ProductImageList.as_view()),
    path('productimages/<int:product_id>', fireviews.ProductImageByProduct.as_view()),
    path('productimagesops/<int:pk>', fireviews.ProductImageDetail.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
