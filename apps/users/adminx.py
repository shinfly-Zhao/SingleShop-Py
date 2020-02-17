"""
@author:zyf
@time:2020/01/08
@filename:adminx.py
"""

import xadmin
from xadmin import views
from .models import *


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "SignleShop管理"
    site_footer = "SignleShop管理"
    menu_style = "accordion"
    apps_icons = {"goods": "fa fa-television",
                  "trade": "fa fa-paypal",

                  'chat': 'fa fa-wechat',

                  }


class UserAddressAdmin():
    list_display = ["user"]


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
