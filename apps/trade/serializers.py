"""
@author:zyf
@time:2020/01/13
@filename:serializers.py
"""

from rest_framework import serializers
from goods.seralizer import GoodsListSerializer
from .models import *
from datetime import datetime ,timedelta


class ShopCartListSerializer(serializers.ModelSerializer):
    # 购物车列表
    goods = GoodsListSerializer(many=False, read_only=True)
    total_fee = serializers.SerializerMethodField()

    def get_total_fee(self, obj):
        return round(obj.nums * obj.goods.shop_price, 2)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums", "total_fee", "id")


class ShopCartCreateSerializer(serializers.Serializer):
    # 购物车数据增加
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    }, help_text="数量")
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), help_text="商品ID")

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSeralizer(serializers.ModelSerializer):
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods

        fields = ("id", "goods_front_image", "name", "shop_price")


class GoodsOrderInfo(serializers.ModelSerializer):
    goods = OrderGoodsSeralizer()

    class Meta:
        model = OrderGoods

        fields = ("goods", "goods_num")


class CreateOrederSerializer(serializers.ModelSerializer):
    #  创建订单
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 创建订单后返回商品数据
    goods = GoodsOrderInfo(many=True,read_only=True)

    cart = serializers.CharField(help_text="购物车id")

    class Meta:
        model = OrderInfo
        fields = ("id", "address", "user", "cart","goodsid","num")

    def create(self,validated_data):
        validated_data["cart"] = validated_data.get("cart",None)
        if validated_data["cart"]:
            # 购物车下单
            validated_data["cart"] = validated_data["cart"].split("-")

            order_mount = 0  # 订单总金额
            for cart in validated_data["cart"]:
                cart = ShoppingCart.objects.get(id=int(cart))
                order_mount += cart.nums * cart.goods.shop_price
            validated_data["order_mount"] = order_mount
            validated_data["cart"] = "-".join(validated_data["cart"])
            # 订单创建时间
            validated_data["add_time"] = datetime.now() + timedelta(hours=8)
            # 创建订单
            order = OrderInfo.objects.create(**validated_data)

            return order
        else:
            # 直接下单
            goods = Goods.objects.get(id=int(validated_data["goodsid"]))
            order_mount = goods.shop_price * int( validated_data["nums"])
            validated_data["order_mount"] = order_mount
            # 订单创建时间
            validated_data["add_time"] = datetime.now() + timedelta(hours=8)
            # 创建订单
            order = OrderInfo.objects.create(**validated_data)
            return order

    def validate(self, attr):
        # 校验购物车
        user = self.context["request"].user
        # 判断是否购物车下单
        cart = attr.get("cart",None)
        goodsid = attr.get("goodsid",None)
        if cart:
            cart = cart.split("-")
            for car in cart:
                shop = ShoppingCart.objects.filter(id=int(car),user=user)
                if shop.exists():
                    continue
                else:
                    raise serializers.ValidationError("购物车错误")
            return attr
        elif goodsid:
            goods = Goods.objects.get(id=int(goodsid))
            if goods:
                nums = attr["nums"]
                if isinstance(nums, int) and nums > 0:
                    return attr
                else:
                    raise serializers.ValidationError("商品数必须大于等于1")
            else:
                raise serializers.ValidationError("商品错误")



































class OrderGoodsSeralizer(serializers.ModelSerializer):
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods

        fields = ("id", "goods_front_image", "name", "shop_price")


class GoodsOrderInfo(serializers.ModelSerializer):
    goods = OrderGoodsSeralizer()

    class Meta:
        model = OrderGoods

        fields = ("goods", "goods_num")


class PayOrederListSerializer(serializers.ModelSerializer):
    # 我的订单列表
    goods = GoodsOrderInfo(many=True)  # 关联订单详情
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OrderInfo
        fields = ("id", "goods", "order_mount", "pay_status", "add_time", "cart","goodsid","nums")    #  cart, goodsid,nums 重新支付使用


class PayOrederUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = ["pay_status"]

    def update(self, instance, validated_data):
        instance.pay_status = validated_data["pay_status"]
        instance.save()
        return instance


class OrderPutSerializer(serializers.Serializer):
    # 微信客户端(小程序)修改订单状态 -- 微信前端发送请求
    order_sn = serializers.CharField()
    msg = serializers.ChoiceField(choices=(
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("TRADE_FINISHED", "交易结束"),
    ))


