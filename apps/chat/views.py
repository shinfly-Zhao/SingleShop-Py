from .serializers import *
from .models import *
from utils.http.XBAPIView import *
from utils.page.page import NewPageSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions.permissions import UserHasMobile


# from .filters import ChatFilter


class BaseChatViewSet(XBListModelMixin,
                      XBCreateModelMixin):
    # 社区
    serializer_class = BaseChatSeralozerListSerializer
    pagination_class = NewPageSetPagination
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # search_fields = ('name',)  # 搜索
    # ordering_fields = ["add_time"]  # 排序
    # filter_class = ChatFilter

    def get_queryset(self):
        my = self.request.query_params.get("my", None)
        if my:
            return BaseChat.objects.filter(user=self.request.user)
        else:
            return BaseChat.objects.all()


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
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class MyChatViewSet(XBListModelMixin):
    # 和我相关的帖子
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        if self.request.query_params.get("my", None):
            mychat = BaseChat.objects.filter(user=self.request.user)  # 我发布的
            allreplay = RreplyBasChat.objects.filter(is_read=False, chat__in=mychat)
            allBaseChat = BaseChat.objects.filter(sub_chat__in=allreplay)
            # 帖子设置已读
            # for replay in allreplay:
            #     replay.is_read = True
            #     replay.save()
            return allBaseChat
        else:
            nums = RreplyBasChat.objects.filter(is_read=False).count()
            return [{"nums": nums}]

    def get_serializer_class(self):
        if self.action == "list" and self.request.query_params.get("my", None):
            return BaseChatSeralozerListSerializer
        else:
            return MyChatSerializers
