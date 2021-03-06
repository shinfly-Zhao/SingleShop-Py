from django.db import models
from goods.models import *
from users.models import UserProfile, UserAddress


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE, help_text="所属用户")
    goods = models.ForeignKey(Goods, verbose_name=u"商品", on_delete=models.CASCADE, help_text="所属商品")
    nums = models.IntegerField(default=0, verbose_name="购买数量", help_text="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),  # 支付成功
        ("TRADE_CLOSED", "超时关闭"),  # 未支付 已关闭
        ("WAIT_BUYER_PAY", "交易创建"), # 未支付
        ("TRADE_FINISHED", "交易结束"),  # 订单完成
        ("PAYING", "待支付"),  # 订单已创建 还未支付
    )

    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="PAYING", max_length=30, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言", null=True, blank=True, unique=True)
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    cart = models.CharField(max_length=100, null=True, blank=True, verbose_name="购物车")
    goodsid = models.CharField(max_length=100, null=True, blank=True, verbose_name="商品")
    nums = models.IntegerField(null=True, blank=True, verbose_name="数量")

    # 用户信息
    address = models.ForeignKey(UserAddress, verbose_name="收货地址", on_delete=models.CASCADE, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", on_delete=models.CASCADE, related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
