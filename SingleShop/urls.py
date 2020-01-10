"""SingleShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
import xadmin
from django.urls import path
from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls  # 文档
import xadmin
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from rest_framework_swagger.views import get_swagger_view
# from rest_framework_jwt.views import obtain_jwt_token
from users.views import *
from goods.views import *
from rest_framework_jwt.views import obtain_jwt_token
from SingleShop.settings import MEDIA_ROOT, STATIC_ROOT

router = DefaultRouter()
router.register("category", GoodsCategoryViewSet, base_name="category")  # 商品分类
router.register("news", NewsViewSet, base_name="news")  # 公告
router.register("banner", BannerViewSet, base_name="banner")  # 轮播图
router.register("goods", GoodsViewSet, base_name="goods")  # 商品
router.register("address", UserAddressViewSet, base_name="address")  # 用户地址
router.register("wxreg", UserRegistViewSet, base_name="wxreg")  # 用户注册

# router.register("reg",UserRegistViewSet,base_name="reg")  # 电话号码注册
# router.register("wxreg", UserWxRegistViewSet,base_name="wxreg")  # 微信注册
schema_view = get_swagger_view(title="Megenex文档")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^sigleshop/', include_docs_urls(title='SigleShop文档')),
    url(r'^swagger/', schema_view),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 媒体文件
    url(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),  # 静态文件
    url(r'^', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_jwt_token),
    url(r'^ueditor/', include("DjangoUeditor.urls")),

]
