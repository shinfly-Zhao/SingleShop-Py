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
    sub_chat = BaseReplayChatSeralozerListSerializer(many=True)
    imgs = serializers.SerializerMethodField()
    user = UserChatSeralizers(many=False)

    def get_imgs(self, instance):
        return instance.imgs.split("##")

    class Meta:
        model = BaseChat
        fields = "__all__"
