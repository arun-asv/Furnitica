# Generated by Django 3.2 on 2021-06-12 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20210612_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='date_added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
