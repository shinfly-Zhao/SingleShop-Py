"""
@author:zyf
@time:2020/01/09
@filename:seralizers.py
"""
import re
from rest_framework import serializers
from users.models import *
from datetime import datetime, timedelta
from utils.http.XBHTTPCode import *
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator




class UserAddressListSerializer(serializers.ModelSerializer):
    # 收获地址列表
    class Meta:
        model = UserAddress

        fields = ("id", "signer_name", "signer_mobile", "province",
                  "city", "district", "address")


class UserAddressCreateSerializer(serializers.ModelSerializer):
    # 创建收获地址
    add_time = serializers.DateField(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = "__all__"


class UserAddressUpdateSerializer(serializers.ModelSerializer):
    # 修改收获地址
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = ("province", "user", "city", "district", "address", "signer_name", "signer_mobile")


class UserWxRegSerializer(serializers.ModelSerializer):
    # 限制用户的输入情况(微信注册)

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserWxRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ("username", "password")