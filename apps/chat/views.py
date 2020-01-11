from .serializers import *
from .models import *
from utils.http.XBAPIView import *
from utils.page.page import NewPageSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class BaseChatViewSet(XBListModelMixin):
    serializer_class = BaseChatSeralozerListSerializer

    queryset = BaseChat.objects.all()