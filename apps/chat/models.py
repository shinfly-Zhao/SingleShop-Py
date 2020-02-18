from django.db import models
from users.models import *


class BaseChat(models.Model):
    # 基本论坛
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    imgs = models.CharField(max_length=2000, verbose_name="图片地址", help_text="图片地址",null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    user = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE, related_name="base_chat")
    is_top = models.CharField(max_length=10, choices=(("top", "置顶"), ("basic", "不置顶")), default="basic",
                              verbose_name="是否置顶")
    is_use = models.BooleanField(default=False, verbose_name="是否通过")

    class Meta:
        verbose_name = '社群管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class RreplyBasChat(models.Model):
    # 回复基本论坛
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    user = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE, related_name='chat_user')
    chat = models.ForeignKey(BaseChat, verbose_name="基础帖子", on_delete=models.CASCADE, null=True, blank=True,
                             related_name="sub_chat")
    tchat = models.ForeignKey("self", verbose_name="所属二级", on_delete=models.CASCADE, null=True, blank=True,
                              related_name="sub_tchat")
    ruser = models.ForeignKey(UserProfile, verbose_name="回复的用户", on_delete=models.CASCADE, related_name='chat_ruser',
                              null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = '回帖管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UserChatFav(models.Model):
    # 用户点赞帖子
    chat = models.ForeignKey(BaseChat, verbose_name="帖子", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '帖子点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chat.title
