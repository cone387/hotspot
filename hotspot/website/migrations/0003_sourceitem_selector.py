# Generated by Django 2.2.4 on 2019-08-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190829_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourceitem',
            name='selector',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='选择器配置'),
        ),
    ]
