# Generated by Django 3.2.13 on 2022-10-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20221018_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlbase',
            name='longUrl',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Исходная ссылка'),
        ),
        migrations.AlterField(
            model_name='urlbase',
            name='shortUrl',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Короткая сслылка'),
        ),
    ]
