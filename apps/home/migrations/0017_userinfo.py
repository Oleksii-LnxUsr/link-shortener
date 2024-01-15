# Generated by Django 3.2.13 on 2022-11-16 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0016_auto_20221115_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastUrl', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Источник перехода')),
                ('shortUrl', models.CharField(blank=True, max_length=255, null=True, verbose_name='Короткая сслылка')),
                ('typeDevice', models.CharField(blank=True, choices=[('none', 'none'), ('mobile', 'mobile'), ('tablet', 'tablet'), ('pc', 'pc')], default='none', max_length=10, null=True, verbose_name='Тип устройства')),
                ('userIP', models.CharField(blank=True, max_length=50, null=True, verbose_name='IP')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('urlBase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.urlbase', verbose_name='Url')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сессии',
                'verbose_name_plural': 'Сессии',
            },
        ),
    ]
