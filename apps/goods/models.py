from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    # 商品类别
    name = models.CharField(max_length=30, verbose_name="类别名称", help_text="类别名称")
    code = models.CharField(max_length=30, verbose_name="类别编码", help_text="类别编码")
    index = models.IntegerField(verbose_name="展示顺序", null=True, blank=True)
    icon = models.ImageField(upload_to="category/icon/", verbose_name="类别图标", help_text="类别图标", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "商品类别管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品类设计
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", on_delete=models.CASCADE, related_name="goods",
                                 help_text="商品类目")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号", help_text="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名", help_text="商品名")
    goods_num = models.IntegerField(default=0, verbose_name="库存数", null=True, blank=True, help_text="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格", help_text="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格", help_text="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述", help_text="商品简短描述")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/goods/images/", width=1000, height=300,
                              filePath="goods/goods/files/", default='', help_text="商品内容")
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费", help_text="是否承担运费")
    goods_front_image = models.ImageField(upload_to="goods/goods/images/", null=True, blank=True, verbose_name="封面图",
                                          help_text="封面图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SingleShopNew(models.Model):
    # 公告管理
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    is_show = models.BooleanField(default=False, verbose_name="是否展示", help_text="是否展示")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class GoodsImage(models.Model):
    """
    商品轮播图 -- 每个商品的小图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE, help_text="商品")
    image = models.ImageField(upload_to="goods/ming", verbose_name="图片", null=True, blank=True, help_text="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播图
    """

    SHOW_TYPE = (
        (1, "首页轮播"),
        (2, "最新活动"),
    )
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE, help_text="商品")
    image = models.ImageField(upload_to='goods/banner/', verbose_name="轮播图片", help_text="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序", help_text="轮播顺序")
    show_type = models.IntegerField(default=1, choices=SHOW_TYPE, verbose_name="展示控制", help_text="展示控制")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class ShopCoupons(models.Model):
    # 商品购物券
    name = models.CharField(max_length=50, verbose_name="介绍", help_text="介绍")
    st_time = models.DateTimeField(verbose_name="开始时间", help_text="开始时间")
    en_time = models.DateTimeField(verbose_name="结束时间", help_text="结束时间")
    lines = models.FloatField(verbose_name="额度", help_text="额度")
    is_use = models.BooleanField(default=True, verbose_name="是否可用", help_text="是否可用")
    nums = models.IntegerField(verbose_name="总数", help_text="总数")
    max = models.FloatField(verbose_name="满额", default=100)

    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PS(models.Model):
    price = models.FloatField(verbose_name="配送费", default=0)
    is_use = models.BooleanField(default=True, verbose_name="是否可用", help_text="是否可用")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '配送费'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.price) + "元配送费设置成功"
