# Generated by Django 3.2 on 2021-07-08 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0029_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(null=True, upload_to='pics/pro'),
        ),
    ]