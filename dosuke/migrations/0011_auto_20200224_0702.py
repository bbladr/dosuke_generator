# Generated by Django 3.0.3 on 2020-02-24 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dosuke', '0010_auto_20200224_0249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='band',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]