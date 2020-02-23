from django.db import models
from django.core import validators

class Event(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=20,
    )

    memo = models.TextField(
        verbose_name='description',
        max_length=300,
        blank=True,
        null=True,
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Event'

class Band(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=20,
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
    )

    memo = models.TextField(
        verbose_name='description',
        max_length=300,
        blank=True,
        null=True,
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Band'
        verbose_name_plural = 'Band'

class Member(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=20,
    )

    entry_year = models.IntegerField(
        verbose_name='entry_year',
        validators=[validators.MinValueValidator(2000)],
    )

    band  = models.ManyToManyField(Band)

    memo = models.TextField(
        verbose_name='description',
        max_length=300,
        blank=True,
        null=True,
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Member'
