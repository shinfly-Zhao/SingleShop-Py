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


class UserAddressViewSet(XBListModelMixin,
                         XBRetrieveModelMixin,
                         XBCreateModelMixin,
                         XBUpdateModelMixin,
                         XBDestroyModelMixin):
    # 用户地址管理
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserAddressListSerializer
        elif self.action == "update":
            return UserAddressUpdateSerializer
        else:
            return UserAddressUpdateSerializer


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


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义登陆返回数据
    """
    if user:
        return {
            'token': token,
            'username': user.mobile,
        }
    else:
        return None


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
