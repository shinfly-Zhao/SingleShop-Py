"""
@author:zyf
@time:2020/01/09
@filename:filters.py
"""

import django_filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    top_category = django_filters.NumberFilter(method="top_category_filter",help_text="商品所属类别id")  # 查找一类商品下的所有商品

    def top_category_filter(self, queryset, name, value):
        """
        :param queryset: 原始数据 来自 get_queryset()
        :param name: 参数名称 top_category
        :param value: 参数值
        :return: 返回符合结果的数据
        """
        return  queryset.filter(Q(category=value)|Q(category__id=value))

    class Meta:
        model = Goods
        fields = ["top_category"]
