from .seralizer import *
from .models import *
from utils.http.XBAPIView import *
from utils.page.page import NewPageSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .filters import *
from user_operation.serializer import *


class GoodsCategoryViewSet(XBListModelMixin):
    """
    list:
        商品类别
    """
    serializer_class = GoodsCategoryListSerizlizer

    def get_queryset(self):
        return GoodsCategory.objects.all().order_by("-index")


class NewsViewSet(XBListModelMixin):
    # 公告
    serializer_class = NewsListSeralizer

    def get_queryset(self):
        return SingleShopNew.objects.filter(is_show=True)


class BannerViewSet(XBListModelMixin):
    # 首页轮播与最新
    serializer_class = BannerSerlizer

    def get_queryset(self):
        return Banner.objects.all().order_by("index")


class GoodsViewSet(XBListModelMixin,
                   XBRetrieveModelMixin):

    serializer_class = GoodsListSerializer
    pagination_class = NewPageSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # 对价格 名称做过滤
    filter_class = GoodsFilter
    # 对商品名称 商品简介以及商品类容做过滤
    # search_fields = ["name","goods_brief",""]

    def get_queryset(self):
        return Goods.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return GoodsListSerializer
        elif self.action == "retrieve":
            return GoodsRetrieveSerializer


class ShopCouponsViewSet(XBListModelMixin,
                         XBCreateModelMixin):
    # 购物券
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        if self.request.query_params.get("my", None):
            return UserCoupons.objects.filter(user=self.request.user)
        else:
            return ShopCoupons.objects.filter(is_use=True)

    def get_serializer_class(self):
        if self.action == "list" and self.request.query_params.get("my", None):
            return MyShopCouponsSerializer
        elif self.action == "list":
            return ShopCouponsSerializer
        elif self.action == "create":
            return UserGetCouponSerializer
        else:
            return ShopCouponsSerializer


