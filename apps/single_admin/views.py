from utils.http.XBAPIView import *
from .serializers import *
from utils.page.page import NewPageSetPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions.permissions import *
from goods.models import *
from rest_framework import status
from SingleShop.settings import UEDITOR_SETTINGS
from django.shortcuts import HttpResponse
import json


class XadminGoodsCategoryViewSet(XBModelViewSet):
    # 商品类别
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return GoodsCategory.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return XadminCategorySerializers
        else:
            return XadminCategoryCreateSerializers


class AdminGoodsViewSet(XBModelViewSet):
    # 商品
    serializer_class = XadminGoodsSerializers
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return Goods.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return XadminGoodsSerializers
        elif self.action == "create":
            return XadminGoodsCreateSerializers
        else:
            return XadminGoodsCreateSerializers


class AdminNewsViewSet(XBModelViewSet):
    # 公告
    serializer_class = NewsListSerializers
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return SingleShopNew.objects.all()


class AdminGoodsInfoImagesViewSet(XBModelViewSet):
    # 商品小图
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return GoodsImage.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return GoodsInfoImagesListSerializers
        elif self.action == "create":
            return GoodsInfoImagesCreateSerializers
        else:
            return GoodsInfoImagesCreateSerializers


class AdminShopCouponsImagesViewSet(XBModelViewSet):
    pagination_class = NewPageSetPagination
    serializer_class = AdminShopCouponsSerializers
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return ShopCoupons.objects.all()


class AdminBannerViewSet(XBModelViewSet):
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserIsAdminOrXadmin]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return Banner.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AdminBannerListSerializers
        else:
            return AdminBannerCreateSerializers


class Up(XBCreateModelMixin,
         XBListModelMixin):

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = self.perform_create(serializer)
            return Response({"state": "SUCCESS",
                             "url": "/media/goods/goods/images/" + name,
                             "title": name,
                             })
        except:
            headers = self.get_success_headers(serializer.data)
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def perform_create(self, serializer):
        name = serializer.save()
        return name

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return []
        else:
            return UpFile

    def list(self, request, *args, **kwargs):
        callback = request.query_params.get("callback", None)
        if callback:
            return HttpResponse(str(callback) + "(" + json.dumps(UEDITOR_SETTINGS) + ")")
        else:
            return HttpResponse("配置错误")
