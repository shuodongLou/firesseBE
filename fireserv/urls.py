
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from fireserv import views as fireviews
from rest_framework.authtoken import views as authviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/users/', fireviews.UserList.as_view()),
    path('api/users/<int:pk>', fireviews.UserDetail.as_view()),
    path('api/accounts/', fireviews.AccountList.as_view()),
    path('api/create_account/', fireviews.create_account),
    path('api/accounts/<int:pk>', fireviews.AccountDetail.as_view()),
    #path('api-token-auth/', authviews.obtain_auth_token),
    path('api/custom-token-auth/', fireviews.CustomObtainToken.as_view()),
    path('api/logout_user/', fireviews.logout_user),
    path('api/change_password/', fireviews.change_password),
    path('api/storeimg/', fireviews.CreatePhoto.as_view()),
    path('api/inquiries/', fireviews.InquiryList.as_view()),
    path('api/inquiries/<int:pk>', fireviews.InquiryDetail.as_view()),
    path('api/inquiriesforuser/<int:acc_id>', fireviews.InquiryListForUser.as_view()),
    path('api/unresolvedinquiries/', fireviews.InquiryListUnresolved.as_view()),
    path('api/getphotobyinquiryid/<int:inq_id>', fireviews.PhotoListById.as_view()),
    path('api/getaccidbyuser/<int:user_id>', fireviews.AccidByUser.as_view()),
    path('api/products/', fireviews.ProductList.as_view()),
    path('api/products/<int:pk>', fireviews.ProductDetail.as_view()),
    path('api/productimages/', fireviews.ProductImageList.as_view()),
    path('api/productimages/<int:product_id>', fireviews.ProductImageByProduct.as_view()),
    path('api/productimagesops/<int:pk>', fireviews.ProductImageDetail.as_view()),
    path('api/agents/', fireviews.AgentList.as_view()),
    path('api/agents/<int:pk>', fireviews.AgentDetails.as_view()),
    path('api/agentsbyaccount/<int:acct_id>', fireviews.AgentListByAccount.as_view()),
    path('api/hasfirecode/', fireviews.hasFirecode),
    path('api/orders/', fireviews.OrderList.as_view()),
    path('api/orders/<int:pk>', fireviews.OrderDetails.as_view()),
    path('api/ordersbyaccount/<int:acct_id>', fireviews.OrderListByAccount.as_view()),
    path('api/orderproducts/', fireviews.OrderProductsList.as_view()),
    path('api/orderproducts/<int:order_id>', fireviews.OrderProductsListByOrder.as_view()),
    path('api/articles/', fireviews.ArticleList.as_view()),
    path('api/articles/<int:pk>', fireviews.ArticleDetails.as_view()),
    path('api/rewards/', fireviews.RewardsByCode.as_view()),
    path('api/wechatpay/', fireviews.wechatPay),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
