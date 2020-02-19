"""
@author:zyf
@time:2020/01/11
@filename:adminx.py
"""


import xadmin
from .models import *


class BaseChatXadmin():
    list_display = ['title', "user", "is_top", "is_use", "add_time", ]
    list_editable = ["is_top", "is_use"]
    list_filter = ["title"]


class ReplayBaseChatXadmin():
    list_display = ['title', "user", "chat"]
    list_filter = ["title"]


class UserFavChatXadmin():
    list_display = ['chat',"user"]


xadmin.site.register(BaseChat,BaseChatXadmin)
xadmin.site.register(RreplyBasChat, ReplayBaseChatXadmin)
xadmin.site.register(UserChatFav,UserFavChatXadmin)