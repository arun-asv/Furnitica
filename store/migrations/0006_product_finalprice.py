# Generated by Django 3.2 on 2021-07-04 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210704_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='finalprice',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]