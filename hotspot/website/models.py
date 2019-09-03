from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

# 一条资讯应该有以下信息。
# 来源于哪里。热度是多少。如何衡量热度？
STATUS = {
    0: '禁用',
    1: '启用'
}


class HotSpot(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    source = models.IntegerField(verbose_name='来源网站ID', db_index=True)
    real_pos = models.IntegerField(verbose_name='实时热度', default=10)
    hot_descr = models.CharField(verbose_name='热度说明', null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_hotspot'
        verbose_name_plural = verbose_name = '采集数据'


class SourceItem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='来源ID')
    category = models.CharField(max_length=20, verbose_name='分类')
    site_name = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='来源网站')
    name = models.CharField(max_length=20, verbose_name='榜名')
    url = models.CharField(max_length=255, unique=True, verbose_name='来源URL')
    fetch_interval = models.IntegerField(default=10, verbose_name='采集频率')
    fetch_time = models.DateTimeField(default=timezone.now, verbose_name='采集时间')
    selector = models.CharField(max_length=200, null=True, blank=True, verbose_name='选择器配置')
    status = models.IntegerField(choices=STATUS.items(), default=1, verbose_name='状态')
    default_count = models.IntegerField(verbose_name='默认返回条数', default=10)
    charset = models.CharField(max_length=5, default='utf-8', verbose_name='网站编码')
    image = models.CharField(max_length=200, verbose_name='图片地址', null=True, blank=True)
    last_runtime = models.DateTimeField(default=timezone.now, verbose_name='最后运行时间')
    abnormal = models.IntegerField(default=0, verbose_name='异常代码')
    warn_msg = models.CharField(max_length=200, null=True, blank=True, verbose_name='异常提醒')
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'config_source'
        verbose_name_plural = verbose_name = '热点源'

    def __str__(self):
        return self.name


class CrawlLog(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='日志自增id')
    source_id = models.IntegerField(verbose_name='来源ID')
    hot_num = models.IntegerField(verbose_name='热点数量')
    upload_num = models.IntegerField(verbose_name='上次成功数量')
    start_time = models.DateTimeField(verbose_name='开始时间')
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_log_website'
        verbose_name_plural = verbose_name = '采集日志'

    def __str__(self):
        return self.source_id


class UserItem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增ID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='用户')
    source = models.ForeignKey(SourceItem, on_delete=models.CASCADE, verbose_name='来源')
    rank = models.IntegerField(verbose_name='顺序')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'data_user'
        verbose_name_plural = verbose_name = '用户热点源'

    def __str__(self):
        return self.user


class History(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增历史ID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='用户')
    source = models.IntegerField(verbose_name='来源')
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'data_user_history'
        verbose_name_plural = verbose_name = '用户历史浏览'

    def __str__(self):
        return self.user


class Collection(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增收藏ID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='用户')
    source = models.IntegerField(verbose_name='来源')
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'data_user_collect'
        verbose_name_plural = verbose_name = '用户收藏'

    def __str__(self):
        return self.user

# 一个用户可以选择多个来源的热点
# 其实吧。我也不知道该怎么办好了。是这样的吗
# 如果说那样的人是不是这样

