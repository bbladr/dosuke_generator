from django.db import models
from django.core import validators
from django_mysql.models import ListCharField

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

class Event(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=20,
    )

    band_list = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11) 
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

# TODO バンドモデル、メンバーモデルを作成し、OneHasMany 関係にする
# class Band(models.Model):

#     name = models.CharField(
#         verbose_name='Name',
#         max_length=20,
#     )

#     member_list = ListCharField(
#         base_field=models.CharField(max_length=10),
#         max_length=30,
#     )

#     memo = models.TextField(
#         verbose_name='description',
#         max_length=300,
#         blank=True,
#         null=True,
#     )

    # # 以下は管理サイト上の表示設定
    # def __str__(self):
    #     return self.name

    # class Meta:
    #     verbose_name = 'Band'
    #     verbose_name_plural = 'Band'

# class Member(models.Model):

#     name = models.CharField(
#         verbose_name='Name',
#         max_length=20,
#     )

#     entry_year = models.IntegerField(
#         verbose_name='entry_year',
#         validators=[validators.MinValueValidator(1)],
#     )

#     memo = models.TextField(
#         verbose_name='description',
#         max_length=300,
#         blank=True,
#         null=True,
#     )

    # # 以下は管理サイト上の表示設定
    # def __str__(self):
    #     return self.name

    # class Meta:
    #     verbose_name = 'Member'
    #     verbose_name_plural = 'Member'
