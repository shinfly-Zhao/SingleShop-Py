from django.shortcuts import render
from utils.http.XBAPIView import *
from .models import *
from utils.permissions.permissions import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import *
from rest_framework_xml.parsers import XMLParser
from rest_framework.views import APIView
from rest_framework import status


# 微信返回的信息为xml
class WechatPaymentXMLParser(XMLParser):
    media_type = 'text/xml'


class ShoppingCartViewSet(XBModelViewSet):
    """
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    update:
        更新购物记录
    """
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication]
    serializer_class = ShopCartListSerializer

    def perform_create(self, serializer):
        # 库存相应减少
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        # 相应库存增多
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        # 购物车商品数量修改
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums-existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return ShopCartCreateSerializer
        else:
            return ShopCartListSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

# ----------------------------------订单支付相关---------------------------------


class CreateOredrViewSet(XBModelViewSet):
    # 订单相关
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user).order_by("-add_time")

    def get_serializer_class(self):
        if self.action == "list":
            return PayOrederListSerializer
        elif self.action == "create":
            return CreateOrederSerializer
        # elif self.action == "put":
        #     return PayOrederRetieveistSerializer
        else:
            return PayOrederListSerializer
        # elif self.action == "retrieve":
        #     return PayOrederRetieveistSerializer
        # else:
        #     return PayOrederUpdateSerializer

    def perform_create(self, serializer):
        # 创建订单 -- 创建订单详情
        order = serializer.save()
        if order.cart:
            carts = order.cart.split("-")
            for cart in carts:
                car = ShoppingCart.objects.get(id=int(cart))
                order_goods = OrderGoods()
                order_goods.goods = car.goods
                order_goods.goods_num = car.nums
                order_goods.order = order
                order_goods.save()
                car.delete()  # 购物车数据待删除
        else:
            # 直接下单的
            order_goods = OrderGoods()
            goods = Goods.objects.get(id=int(order.gooids))
            order_goods.goods = goods
            order_goods.goods_num = order.nums
            order_goods.order = order
            order_goods.save()

    def perform_update(self, serializer):
        instance = serializer.save()


class GetWxCode(APIView):
    # 微信异步通知
    parser_classes = [WechatPaymentXMLParser]

    def post(self,request):
        # 微信异步通知支付结果  -- 修改状态为已付款
        postdata = self.request.data
        if postdata["return_code"] and postdata["result_code"] == "SUCCESS":
            out_trade_no = postdata["out_trade_no"]
            transaction_id = postdata["transaction_id"]
            order = OrderInfo.objects.get(order_sn=out_trade_no)
            if order:
                order.trade_no = transaction_id
                order.pay_status = "TRADE_SUCCESS"
                order.save()
        data = "<xml><return_code><![CDATA[SUCCESS]]>\
               </return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
        return Response(data,content_type="text/xml")

    def get(self, request):

        data = "<xml><return_code><![CDATA[SUCCESS]]>\
                       </return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
        return Response(data, content_type="text/xml")


class PutPayCode(APIView):
    """
    put:
        微信客户端修改订单状态
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = OrderPutSerializer

    def put(self, request):
        try:
            order_sn = self.request.data["order_sn"]
            msg = self.request.data["msg"]
            if msg in ["TRADE_SUCCESS", "TRADE_CLOSED","WAIT_BUYER_PAY",
                        "TRADE_FINISHED","PAYING"]:
                Order = OrderInfo.objects.filter(order_sn=order_sn,user = self.request.user)
                if Order:
                    Order[0].pay_status = msg
                    Order[0].save()
                    return Response(status=status.HTTP_200_OK, data={
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
                            "msg": "success"
                        }})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4004_CAN_NO_FIND.value,
                            "msg": "找不到"
                        }})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "status": {
                        "code": ResponseSatatusCode.HTTPCODE_1006_PARAMETER_VALUE_ERROR.value,
                        "msg": ["TRADE_SUCCESS", "TRADE_CLOSED","WAIT_BUYER_PAY",
                                "TRADE_FINISHED","PAYING"]
                    }})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_1001_PARAMETER_ERROR.value,
                    "msg": "参数错误"
                }})

