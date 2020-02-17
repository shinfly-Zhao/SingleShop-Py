from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    utype = models.CharField(default="members", max_length=50, choices=(("members", "会员"), ("admin", "管理员")),
                             verbose_name="用户类型")
    user_font = models.ImageField(upload_to="user/font/", null=True, blank=True, verbose_name="用户头像")
    nick_name = models.CharField(max_length=100, verbose_name="用户昵称", default="暂无昵称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户" ,on_delete=models.CASCADE)
    province = models.CharField(max_length=100, verbose_name="省份",help_text="省份")
    city = models.CharField(max_length=100, verbose_name="城市",help_text="城市")
    district = models.CharField(max_length=100, verbose_name="区域",help_text="区域")
    address = models.CharField(max_length=100, verbose_name="详细地址",help_text="详细地址")
    signer_name = models.CharField(max_length=100, verbose_name="签收人",help_text="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="电话",help_text="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")


    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code