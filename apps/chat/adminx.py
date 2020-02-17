"""
@author:zyf
@time:2020/01/11
@filename:adminx.py
"""


import xadmin
from .models import *


class BaseChatXadmin():
    list_display = ['title', "user", "tchat", "ruser", "add_time"]


class ReplayBaseChatXadmin():
    list_display = ['title', "user", "chat"]


class UserFavChatXadmin():
    list_display = ['chat',"user"]


xadmin.site.register(BaseChat,BaseChatXadmin)
xadmin.site.register(RreplyBasChat,ReplayBaseChatXadmin)
xadmin.site.register(UserChatFav,UserFavChatXadmin)