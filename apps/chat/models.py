from django.db import models
from users.models import *


class BaseChat(models.Model):
    # 基本论坛
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    imgs = models.CharField(max_length=2000,verbose_name="图片地址", help_text="图片地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    user = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE, related_name="base_chat")

    class Meta:
        verbose_name = '社群管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class RreplyBasChat(models.Model):
    # 回复基本论坛
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    imgs = models.CharField(max_length=2000,verbose_name="图片地址", help_text="图片地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    user = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE)
    chat = models.ForeignKey(BaseChat, verbose_name="基础帖子", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="所属回帖", help_text="所属回帖",
                                        related_name="sub_cat", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '回帖管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title












