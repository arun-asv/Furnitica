# Generated by Django 3.2 on 2021-07-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0023_auto_20210705_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
