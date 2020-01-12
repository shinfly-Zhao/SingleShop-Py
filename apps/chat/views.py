from .serializers import *
from .models import *
from utils.http.XBAPIView import *
from utils.page.page import NewPageSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class BaseChatViewSet(XBListModelMixin,
                      XBCreateModelMixin):
    # 社区
    serializer_class = BaseChatSeralozerListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        my = self.request.query_params.get("my", None)
        if my:
            return BaseChat.objects.filter(user=self.request.user)
        else:
            return BaseChat.objects.all()
    queryset = BaseChat.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BaseChatSeralozerListSerializer
        elif self.action == "create":
            return BaseChatCreateSerializer
        else:
            return BaseChatSeralozerListSerializer


class ReBaseChatViewSet(XBCreateModelMixin):
    # 社区回复
    serializer_class = ReplayChatCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

