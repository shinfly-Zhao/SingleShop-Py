from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework import mixins, viewsets,status
from .seralizers import *
from random import choice
from utils.mobile_code.YunPian import YunPian
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.exceptions import ErrorDetail, ValidationError
from utils.http.XBAPIView import *
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated  # 权限判断
from .models import *
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from SingleShop.settings import MPBILEAPIKEY


class UserAddressViewSet(XBModelViewSet):
    """
    list:
        地址列表
    create:
        新增地址
    retrieve:
        地址详情
    update:
        地址修改
    delete:
        地址删除
    """
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by("-is_default")

    def get_serializer_class(self):
        if self.action == "list":
            return UserAddressListSerializer
        elif self.action == "update":
            return UserAddressUpdateSerializer
        elif self.action == "create":
            return UserAddressCreateSerializer
        else:
            return UserAddressListSerializer

    def perform_update(self, serializer):
        alluseradd = UserAddress.objects.filter(user=self.request.user)
        if alluseradd:
            for add in alluseradd:
                add.is_default = False
                add.save()
            else:
                pass
        else:
            pass
        instance = serializer.save()
        instance.is_default = True
        instance.save()


class CustomBackend(ModelBackend):
    """
    自定义用户登陆
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:

            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))

            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            raise ValidationError(error_msg("用户名或密码错误"))


class UserRegistViewSet(XBCreateModelMixin):
    """
    用户注册(微信注册)
    """
    serializer_class = UserWxRegSerializer

    def create(self, request, *args, **kwargs):
        method = self.request.META["REQUEST_METHOD"].lower()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            headers = self.get_success_headers(serializer.data)
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST, headers=headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return CodeStatus(type=method,data=re_dict,header=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class SmsCodeViewSet(XBCreateModelMixin):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            headers = self.get_success_headers(serializer.data)
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST, headers=headers)
        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(MPBILEAPIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            # 发送失败
            return Response(status=status.HTTP_400_BAD_REQUEST,data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_4001_UNAUTHORIZED.value,
                    "msg": sms_status["msg"]
                }
            })
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response(status=status.HTTP_201_CREATED,data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_2001_CREATED.value,
                    "msg": "success"
                }
            })


class UserBingdingMobileViewSet(XBCreateModelMixin):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = MobileBinding