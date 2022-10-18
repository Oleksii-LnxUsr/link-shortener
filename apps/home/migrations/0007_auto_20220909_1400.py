# Generated by Django 3.2.13 on 2022-09-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20220908_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheduler',
            name='email_input',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Email, введенный'),
        ),
        migrations.AddField(
            model_name='sheduler',
            name='phone_input',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон, введенный'),
        ),
        migrations.AddField(
            model_name='sheduler',
            name='username_input',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя пользователя, введенное'),
        ),
    ]
