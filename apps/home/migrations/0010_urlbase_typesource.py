# Generated by Django 3.2.13 on 2022-10-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20221019_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlbase',
            name='typeSource',
            field=models.CharField(blank=True, choices=[('www', 'www'), ('api', 'api')], default='www', max_length=10, null=True, verbose_name='Источник'),
        ),
    ]
