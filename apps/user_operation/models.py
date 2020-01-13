from django.db import models
from users.models import *
from goods.models import *


class UserCoupons(models.Model):
    # 用户获取优惠券
    user = models.ForeignKey(UserProfile, verbose_name="所属用户",help_text="所属用户",on_delete=models.CASCADE)
    coupon = models.ForeignKey(ShopCoupons, verbose_name="购物券",help_text="购物券",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")

    class Meta:
        verbose_name = "用户-购物券"
        verbose_name_plural = verbose_name
        unique_together = ("user", "coupon")

    def __str__(self):
        return self.user.username
