"""
@author:zyf
@time:2019/09/02
@filename:xb_Response.py
"""
from rest_framework import mixins, viewsets
from .XBHTTPCode import CodeStatus
from rest_framework import status
from utils.http.XBHTTPCode import error_msg
from rest_framework_jwt.views import *
from .XBHTTPCode import ResponseSatatusCode
from rest_framework import exceptions, status


class XBListModelMixin(viewsets.GenericViewSet,
                       mixins.ListModelMixin):
    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN


        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)


        if response is None:
            self.raise_uncaught_exception(exc)
        response.exception = True
        response.data = {
            "status": {
                "code": ResponseSatatusCode.HTTPCODE_4001_UNAUTHORIZED.value,
                "msg": "Unauthorized"
            }}
        return response


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

        method = self.request.META["REQUEST_METHOD"].lower()
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return CodeStatus(type=method, data=serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_4004_NO_FIND.value,
                    "msg": "无效页面"
                }})


class XBCreateModelMixin(viewsets.GenericViewSet,
                         mixins.CreateModelMixin):
    """
    创建资源
    """

    def create(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_2004_NO_CONTENT.value,
                    "msg": "success"
                }})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_4004_NO_FIND.value,
                    "msg": "未找到"
                }})



    def perform_destroy(self, instance):
        instance.delete()


class XBUpdateModelMixin(mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

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

        return CodeStatus(type=method, data=serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class XBModelViewSet(XBListModelMixin,
                   XBCreateModelMixin,
                   XBRetrieveModelMixin,
                   XBDestroyModelMixin,
                   XBUpdateModelMixin):
    pass


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义登陆返回数据
    """
    if user:
        return {

            "status": {
                "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
                "msg": "success"
            },
            "data": {
                'token': token,
                'username': user.mobile}
        }
    else:
        return None


class XBObtainJSONWebToken(ObtainJSONWebToken):
    # 自定义登陆视图
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(error_msg(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
