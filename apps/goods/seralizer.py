"""
@author:zyf
@time:2020/01/08
@filename:seralizer.py
"""

from rest_framework import serializers
from .models import *
from user_operation.models import UserCoupons
from SingleShop.settings import PAYMONEY

class GoodsCategoryListSerizlizer(serializers.ModelSerializer):
    # 首页常规类别展示
    icon = serializers.SerializerMethodField()

    def get_icon(self,instance):
        return "/media/"+str(instance.icon)
    class Meta:
        model = GoodsCategory
        fields = ["id", "name", "icon", "code"]


class NewsListSeralizer(serializers.ModelSerializer):
    # 公告管理
    class Meta:
        model = SingleShopNew
        fields = ["title"]


class BannerSerlizer(serializers.ModelSerializer):
    """
    首页轮播序列化
    """
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return "/media/" + str(obj.image)

    class Meta:
        model = Banner
        fields = ("id", 'image', "goods", "show_type")


class GoodsListSerializer(serializers.ModelSerializer):
    """
    商品列表序列化
    """

    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods
        fields = ('id', 'name', 'market_price', 'shop_price', "goods_front_image")


class GoodsImagesSerializer(serializers.ModelSerializer):
    """
    商品小轮播
    """
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return "/media/" + str(obj.image)

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsRetrieveSerializer(serializers.ModelSerializer):
    """
    商品详情序列化
    """
    images = GoodsImagesSerializer(many=True)  # 轮播图片
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, instance):
        return "/media/" + str(instance.goods_front_image)

    ps = serializers.SerializerMethodField(read_only=True)

    def get_ps(self, instance):
        return PAYMONEY

    class Meta:
        model = Goods
        fields = ('id', 'name', 'market_price', 'shop_price', "images", "category", "goods_front_image", "ps")


class ShopCouponsSerializer(serializers.ModelSerializer):
    st_time = serializers.DateTimeField(format="%Y-%m-%d")
    en_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = ShopCoupons
        fields = ["id", "name", "st_time", "en_time", "lines", "max"]


class MyShopCouponsSerializer(serializers.ModelSerializer):
    coupon = ShopCouponsSerializer(many=False)

    class Meta:
        model = UserCoupons
        fields = "__all__"