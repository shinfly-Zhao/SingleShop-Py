"""
@author:zyf
@time:2020/01/11
@filename:serializers.py
"""

from rest_framework import serializers
from .models import *


class UserChatSeralizers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user_font", "nick_name"]


class ThreeBaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    user = UserChatSeralizers(many=False)

    class Meta:
        model = RreplyBasChat
        fields = "__all__"


class TwoBaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    sub_cat = ThreeBaseReplayChatSeralozerListSerializer(many=True)

    class Meta:
        model = RreplyBasChat
        fields = "__all__"


class BaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    sub_cat = TwoBaseReplayChatSeralozerListSerializer(many=True)
    user = UserChatSeralizers(many=False)

    class Meta:
        model = RreplyBasChat
        fields = "__all__"


class BaseChatSeralozerListSerializer(serializers.ModelSerializer):
    # 社群列表
    sub_chat = BaseReplayChatSeralozerListSerializer(many=True)
    imgs = serializers.SerializerMethodField()
    user = UserChatSeralizers(many=False)
    is_fav = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S")

    def get_is_fav(self,instance):
        fav = UserChatFav.objects.filter(user=self.context["request"].user,chat=instance)
        if fav:
            return 1
        else:
            return 0

    def get_imgs(self, instance):
        return instance.imgs.split("##")

    class Meta:
        model = BaseChat
        fields = "__all__"


class BaseChatCreateSerializer(serializers.ModelSerializer):
    # 社群发布信息
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BaseChat
        fields = ["title","user","imgs"]


class ReplayChatCreateSerializer(serializers.ModelSerializer):
    # 社群回复
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = RreplyBasChat
        fields = ["title", "user", "parent","chat"]
