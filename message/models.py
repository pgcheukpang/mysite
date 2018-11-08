from django.db import models


class MsgManager(models.Manager):
    def get_queryset(self):
        return super(MsgManager, self).get_queryset().filter(is_deleted=False)


class LeaveMessage(models.Model):
    content = models.TextField(verbose_name='留言内容')
    messager = models.ForeignKey("users.User", verbose_name="留言者", related_name="himself_msg_set")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    reviewed_status = models.CharField(max_length=2, default="0", verbose_name="复审状态")  # 0: 无需复审, 1: 复审已通过, 2: 需要复审
    reviewed_content = models.CharField(max_length=128, blank=True, null=True, verbose_name="复审内容")
    is_error_occured = models.CharField(max_length=2, default="0", verbose_name="是否异常")  # 0: 无异常, 1: 出现异常
    error_msg = models.CharField(max_length=128, blank=True, null=True, verbose_name="异常信息")
    favorites = models.ManyToManyField("users.User", verbose_name='点赞', related_name="like_msg_set")
    is_deleted = models.BooleanField(default=False, verbose_name="数据是否删除")
    # 自定义的管理器
    objects = MsgManager()

    def __str__(self):
        return self.content[:20]
