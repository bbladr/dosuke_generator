from django.db import models
from django.core import validators


class Item(models.Model):

    SEX_CHOICES = (
        (1, 'male'),
        (2, 'female'),
    )

    name = models.CharField(
        verbose_name='name',
        max_length=200,
    )
    age = models.IntegerField(
        verbose_name='age',
        validators=[validators.MinValueValidator(1)],
        blank=True,
        null=True,
    )
    sex = models.IntegerField(
        verbose_name='sex',
        choices=SEX_CHOICES,
        default=1
    )
    memo = models.TextField(
        verbose_name='description',
        max_length=300,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='created_at',
        auto_now_add=True
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Item'
