"""
@author:zyf
@time:2020/01/11
@filename:serializers.py
"""

from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta


class UserChatSeralizers(serializers.ModelSerializer):
    user_font = serializers.SerializerMethodField()

    def get_user_font(self, instance):
        return "/media/" + str(instance.user_font)

    class Meta:
        model = UserProfile
        fields = ["user_font", "nick_name", "id"]


class ThreeBaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    user = UserChatSeralizers(many=False)
    class Meta:
        model = RreplyBasChat
        fields = "__all__"


# 社群列表
class TwoBaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    sub_cat = ThreeBaseReplayChatSeralozerListSerializer(many=True)
    user = UserChatSeralizers(many=False)
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S")

    class Meta:
        model = RreplyBasChat
        fields = "__all__"


class BaseReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    user = UserChatSeralizers(many=False)
    class Meta:
        model = RreplyBasChat
        fields = ["chat", "user", "ruser", "title"]


class BaseChatSeralozerListSerializer(serializers.ModelSerializer):
    # 社群列表
    sub_chat = BaseReplayChatSeralozerListSerializer(many=True)
    imgs = serializers.SerializerMethodField()
    user = UserChatSeralizers(many=False)
    is_fav = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S")
    fav_nums = serializers.SerializerMethodField()

    def get_fav_nums(self, instance):
        return UserChatFav.objects.filter(chat__id=instance.id).count()

    def get_is_fav(self, instance):
        fav = UserChatFav.objects.filter(user=self.context["request"].user, chat=instance)
        if fav:
            return 1
        else:
            return 0

    def get_imgs(self, instance):
        return []
        # print(len(instance.imgs))
        # if len(instance.imgs) > 0:
        #     return instance.imgs.split("##")
        # else:
        #     return []

    class Meta:
        model = BaseChat
        fields = ["id", "sub_chat", "imgs", "user", "title", "fav_nums", "add_time", "is_fav", "is_top"]


class BaseChatCreateSerializer(serializers.ModelSerializer):
    # 社群发布信息
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = BaseChat
        fields = ["title", "user", "imgs"]

    def create(self, validate_data):
        validate_data["add_time"] = (datetime.now() + timedelta(hours=8))
        basechat = BaseChat.objects.create(**validate_data)
        return basechat


class ReplayChatCreateSerializer(serializers.ModelSerializer):
    # 社群回复
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    user_name = serializers.SerializerMethodField(read_only=True)
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S", read_only=True)

    def get_user_name(self, instance):
        return str(self.context["request"].user.nick_name)

    class Meta:
        model = RreplyBasChat
        fields = ["title", "user", "ruser", "chat", "user_name", "tchat", "add_time"]


class MyChatSerializers(serializers.Serializer):

    nums = serializers.IntegerField()


class ChatFavSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserChatFav
        fields = "__all__"

    def create(self, validated_data):
        userFav = UserChatFav.objects.filter(chat=validated_data["chat"])
        if userFav:
            userFav.delete()
            userFav.chat = validated_data["chat"]
        else:
            userFav = UserChatFav.objects.create(**validated_data)

        return userFav


# 社群

class Three(serializers.ModelSerializer):
    user = UserChatSeralizers(many=False)
    ruser = UserChatSeralizers(many=False)
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S")

    class Meta:
        model = RreplyBasChat
        fields = ["title", "user", "ruser", "add_time"]


class BaseChatReplayChatSeralozerListSerializer(serializers.ModelSerializer):
    user = UserChatSeralizers(many=False)
    ruser = UserChatSeralizers(many=False)
    sub_tchat = Three(many=True)
    add_time = serializers.DateTimeField(format="%Y-%d-%d %H:%M:%S")

    class Meta:
        model = RreplyBasChat
        fields = ["id", "chat", "user", "ruser", "sub_tchat", "title", "add_time"]


class BaseChatReplaySeralozerListSerializer(serializers.ModelSerializer):
    sub_chat = BaseChatReplayChatSeralozerListSerializer(many=True)
    imgs = serializers.SerializerMethodField()
    user = UserChatSeralizers(many=False)
    is_fav = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    fav_nums = serializers.SerializerMethodField()

    def get_fav_nums(self, instance):
        return UserChatFav.objects.filter(chat__id=instance.id).count()

    def get_is_fav(self, instance):
        fav = UserChatFav.objects.filter(user=self.context["request"].user, chat=instance)
        if fav:
            return 1
        else:
            return 0

    def get_imgs(self, instance):
        if len(instance.imgs) > 0:
            return instance.imgs.split("##")
        else:
            return []

    class Meta:
        model = BaseChat
        fields = ["id", "sub_chat", "imgs", "user", "title", "fav_nums", "add_time", "is_fav", "is_top"]
