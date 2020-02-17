"""
@author:zyf
@time:2020/01/08
@filename:adminx.py
"""
import xadmin
from .models import *


class GoodsCategoryAdmin():
    # 商品类别
    list_display = ["name", "code", "icon", "add_time"]
    list_filter = ["name"]


class GoodsAdmin():
    # 商品
    list_display = ["name", "category", "goods_num", "shop_price", "market_price"]
    style_fields = {"goods_desc": "ueditor"}
    show_detail_fields = ['category']


class SingleShopNewAdmin():
    # 公告
    list_display = ["title", "is_show", "add_time"]
    list_editable = ["title", 'is_show']


class ImgBannerAdmin():
    # 轮播和热点管理
    list_display = ["goods", "index", "show_type"]
    list_editable = ["goods", 'index']


class GoodsBannerXadmin():
    # 商品轮播小图序列化
    list_display = ["goods", "image"]


class ShopCouponsXadmin():
    # 购物券
    list_display = ["name", "nums", "max", "lines", "st_time", "en_time"]

xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(SingleShopNew, SingleShopNewAdmin)
xadmin.site.register(Banner, ImgBannerAdmin)
xadmin.site.register(GoodsImage, GoodsBannerXadmin)
xadmin.site.register(ShopCoupons, ShopCouponsXadmin)
