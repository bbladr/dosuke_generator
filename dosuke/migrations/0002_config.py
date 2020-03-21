# Generated by Django 3.0.3 on 2020-03-21 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuke', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, verbose_name='key')),
                ('value', models.TextField(max_length=300, verbose_name='value')),
                ('memo', models.TextField(blank=True, max_length=300, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Band',
                'verbose_name_plural': 'Band',
            },
        ),
    ]