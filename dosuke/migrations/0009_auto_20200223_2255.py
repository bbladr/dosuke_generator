# Generated by Django 3.0.3 on 2020-02-23 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dosuke', '0008_band_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='band',
            name='member_list',
        ),
        migrations.RemoveField(
            model_name='event',
            name='band_list',
        ),
    ]