# Generated by Django 3.2.13 on 2022-09-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20220908_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='its_email',
            field=models.BooleanField(default=True, verbose_name='Спросить email'),
        ),
        migrations.AddField(
            model_name='org',
            name='its_name',
            field=models.BooleanField(default=True, verbose_name='Спросить имя'),
        ),
        migrations.AddField(
            model_name='org',
            name='its_phone',
            field=models.BooleanField(default=True, verbose_name='Спросить телефон'),
        ),
    ]
