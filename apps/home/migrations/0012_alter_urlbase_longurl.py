# Generated by Django 3.2.13 on 2022-10-31 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_urlbase_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlbase',
            name='longUrl',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Исходная ссылка'),
        ),
    ]
