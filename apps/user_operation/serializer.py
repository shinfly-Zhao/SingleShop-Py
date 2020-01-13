"""
@author:zyf
@time:2020/01/13
@filename:serializer.py
"""

from rest_framework import serializers
from .models import *


class UserGetCouponSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserCoupons
        fields = ["coupon","user"]