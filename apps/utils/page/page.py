"""
@author:zyf
@time:2019/09/08
@filename:page.py
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework.response  import Response
from collections import OrderedDict, namedtuple


class PageSetPagination(PageNumberPagination):
    """
    分页处理
    """
    page_size_query_description = "每页记录"
    page_query_description = "页码"
    page_size = 2  # 前台可以自定义每页显示的数量
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 1000


class NewPageSetPagination(PageNumberPagination):
    """
    分页处理
    """
    page_size_query_description = "每页记录"
    page_query_description = "页码"
    page_size = 15  # 前台可以自定义每页显示的数量
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_response(self, data):
        if len(data) > 0:
            status = 1
        else:
            status = 0
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ("status",status),
            ("hint","yes")
        ]))
