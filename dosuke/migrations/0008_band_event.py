# Generated by Django 3.0.3 on 2020-02-23 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dosuke', '0007_member_band'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dosuke.Event'),
        ),
    ]