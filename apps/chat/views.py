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
from django.db.models import Q


class BaseChatViewSet(XBListModelMixin,
                      XBCreateModelMixin):
    # 社区
    serializer_class = BaseChatSeralozerListSerializer
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)  # 搜索

    def get_queryset(self):
        time = int(self.request.query_params.get("time", "0"))
        if time in [3, 7, 30, 90]:
            pass
        else:
            time = None
        my = self.request.query_params.get("my", None)
        num = self.request.query_params.get("num", None)
        replay = self.request.query_params.get("replay", None)
        if my:
            self.pagination_class = NewPageSetPagination
            return BaseChat.objects.filter(user=self.request.user).order_by("-add_time")
        elif num:
            nums = RreplyBasChat.objects.filter(is_read=False, ruser=self.request.user).count()
            return [{"nums": nums}]
        elif replay:
            self.pagination_class = NewPageSetPagination
            allreplay = RreplyBasChat.objects.filter(is_read=False, ruser=self.request.user)
            # 查找对应的二级
            two_list = []
            for replay in allreplay:
                two_list.append(replay.tchat)
            # for replay in allreplay:
            #
            allBaseChat = BaseChat.objects.filter(sub_chat__in=two_list).order_by("-add_time")
            # 帖子设置已读
            # for replay in allreplay:
            #     replay.is_read = True
            #     replay.save()
            return allBaseChat
        else:
            self.pagination_class = NewPageSetPagination
            if time:
                time = (datetime.now() - timedelta(days=time))
                now = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")
                now = datetime.strptime(now + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                return BaseChat.objects.filter(add_time__range=(time, now)).order_by("-add_time")
            else:
                return BaseChat.objects.all().order_by("-add_time")

    def get_serializer_class(self):
        if self.action == "create":
            return BaseChatCreateSerializer
        elif self.action == "list" and self.request.query_params.get("num", None):
            return MyChatSerializers
        elif self.action == "list" and self.request.query_params.get("replay", None):
            return BaseChatReplaySeralozerListSerializer
        else:
            return BaseChatReplaySeralozerListSerializer


class ReBaseChatViewSet(XBCreateModelMixin):
    # 社区回复
    serializer_class = ReplayChatCreateSerializer
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class ChatFavViewSet(XBCreateModelMixin):
    serializer_class = ChatFavSerializers
    permission_classes = [IsAuthenticated, UserHasMobile]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
