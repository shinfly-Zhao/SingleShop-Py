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
from SingleShop.settings import REGEX_MOBILE


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
    # (微信注册)
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


class MobileBinding(serializers.ModelSerializer):
    # 限制用户的输入情况

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    def create(self, validated_data):
        user = self.context["request"].user
        user.mobile = validated_data["mobile"]
        user.save()
        return user

    def validate_code(self, code):

        # 检验验证码的正确性
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]  # 获取到最后一个验证码

            five_mintes_ago = datetime.now() - timedelta(hours=8, minutes=15, seconds=0)  # 5分钟之前的时间
            five_mintes_ago = five_mintes_ago.strftime("%Y-%m-%d-%H-%M")
            last = last_record.add_time.strftime("%Y-%m-%d-%H-%M")
            if five_mintes_ago > last:  # 前五分钟的时间如果大于真正注册的时间就当成过期
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]  # 删除验证码
        return attrs

    class Meta:
        model = UserProfile
        fields = ("user", "code", "mobile")


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, help_text="电话号码")

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 手机是否注册
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # one_mintes_ago 表示一分钟之前的时间
        one_mintes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送还未超过60s")
        return mobile