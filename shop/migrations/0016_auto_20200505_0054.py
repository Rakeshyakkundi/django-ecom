# Generated by Django 3.0.5 on 2020-05-05 06:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20200504_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
