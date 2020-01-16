"""
@author:zyf
@time:2020/01/13
@filename:serializers.py
"""
from rest_framework import serializers
from goods.models import *
from SingleShop.settings import BASE_DIR


class XadminCategorySerializers(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField(read_only=True)

    def get_icon(self, instance):
        return "/media/" + str(instance.icon)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class XadminCategoryCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class XadminGoodsSerializers(serializers.ModelSerializer):
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, instance):
        return "/media/" + str(instance.goods_front_image)

    class Meta:
        model = Goods
        fields = "__all__"


class XadminGoodsCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"


class NewsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SingleShopNew
        fields = "__all__"


class GoodsInfoImagesListSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, instance):
        return "/media/" + str(instance.image)

    class Meta:
        model = GoodsImage
        fields = "__all__"


class GoodsInfoImagesCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = "__all__"


class AdminShopCouponsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopCoupons
        fields = "__all__"


class AdminBannerListSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, instance):
        return "/media/" + str(instance.image)

    class Meta:
        model = Banner
        fields = "__all__"


class AdminBannerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class UpFile(serializers.Serializer):
    upfile = serializers.FileField()

    def create(self, validated_data):
        try:
            image = validated_data["upfile"]
            name = validated_data["upfile"].name
            import os
            file = open(os.path.join(BASE_DIR, "media", "goods", "goods", "images", name), 'wb')
            for chunk in image.chunks():
                file.write(chunk)
            file.close()
            return name
        except:
            raise serializers.ValidationError("参数错误")


class UpFileList(serializers.Serializer):
    bd__editor__8nqbon = serializers.JSONField()
