"""
@author:zyf
@time:2020/02/17
@filename:adminx.py
"""

from .models import *
import xadmin


class ShoppingCartAdmin():
    # 商品类别
    list_display = ["user", "goods", "nums"]


class OrderXadmin():
    list_display = ["user", "order_sn", "trade_no", "pay_status", "order_mount"]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderXadmin)
