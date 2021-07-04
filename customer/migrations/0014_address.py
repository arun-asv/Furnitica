# Generated by Django 3.2 on 2021-06-15 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_auto_20210614_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('address1', models.CharField(max_length=250)),
                ('address2', models.CharField(max_length=250)),
                ('mobile', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
            ],
        ),
    ]
