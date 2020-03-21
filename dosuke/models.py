from django.db import models
from django.core import validators

class Member(models.Model):

    name = models.CharField(
        verbose_name='名前',
        max_length=20,
    )

    entry_year = models.IntegerField(
        verbose_name='入部年度',
        validators=[validators.MinValueValidator(2000)],
    )

    memo = models.TextField(
        verbose_name='メモ',
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

class Band(models.Model):

    name = models.CharField(
        verbose_name='バンド名',
        max_length=20,
    )

    members = models.ManyToManyField(
        Member, 
        verbose_name='メンバー',
        blank=False,
    )

    memo = models.TextField(
        verbose_name='メモ',
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

class Config(models.Model):

    key = models.CharField(
        verbose_name='key',
        max_length=20,
    )

    value = models.TextField(
        verbose_name='value',
        max_length=300,
        blank=False,
    )

    memo = models.TextField(
        verbose_name='description',
        max_length=300,
        blank=True,
        null=True,
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Config'
