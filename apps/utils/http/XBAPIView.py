"""
@author:zyf
@time:2019/09/02
@filename:xb_Response.py
"""
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from .XBHTTPCode import CodeStatus
from rest_framework import status
from .XBHTTPCode import ResponseSatatusCode
from rest_framework.renderers import TemplateHTMLRenderer
from utils.http.XBHTTPCode import error_msg


class XBListModelMixin(viewsets.GenericViewSet,
                       mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, 'a')
        method = self.request.META["REQUEST_METHOD"].lower()
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except:
            return CodeStatus(type=method, data=None)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return CodeStatus(type=method, data=serializer.data)


class XBRetrieveModelMixin(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve:
            详情处理
        """
        method = self.request.META["REQUEST_METHOD"].lower()
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return CodeStatus(type=method, data=serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_40004_NOT_FIND.value,
                    "msg": "无效页面"
                }})


class XBCreateModelMixin(viewsets.GenericViewSet,
                         mixins.CreateModelMixin):
    """
    创建资源
    """

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            method = self.request.META["REQUEST_METHOD"].lower()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return CodeStatus(type=method, data=serializer.data)
        except:
            headers = self.get_success_headers(serializer.data)
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST, headers=headers)


class XBDestroyModelMixin(viewsets.GenericViewSet,
                          mixins.DestroyModelMixin):
    """
    删除对象
    """

    def destroy(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_2004_NO_CONTENT.value,
                    "msg": "未找到"
                }})

        return Response(status=status.HTTP_204_NO_CONTENT, data={
            "status": {
                "code": ResponseSatatusCode.HTTPCODE_2004_NO_CONTENT.value,
                "msg": "success"
            }})

    def perform_destroy(self, instance):
        instance.delete()


class XBUpdateModelMixin(mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    更新对象
    """

    def update(self, request, *args, **kwargs):
        method = self.request.META["REQUEST_METHOD"].lower()
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_2004_NO_CONTENT.value,
                    "msg": "未找到"
                }})

        try:

            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except:
            headers = self.get_success_headers(serializer.data)
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST, headers=headers)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return CodeStatus(type=method, data=serializer.data, html=self.html)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
