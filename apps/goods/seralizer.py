"""
@author:zyf
@time:2020/01/08
@filename:seralizer.py
"""

from rest_framework import serializers
from .models import *


class GoodsCategoryListSerizlizer(serializers.ModelSerializer):
    # 首页常规类别展示
    class Meta:
        model = GoodsCategory
        fields = ["name", "icon", "code"]


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

    class Meta:
        model = Goods
        fields = ('id', 'name', 'market_price', 'shop_price', "images")


class ShopCouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCoupons
        fields = "__all__"
