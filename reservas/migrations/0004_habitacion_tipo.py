# Generated by Django 3.0.4 on 2020-03-08 23:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_auto_20200308_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitacion',
            name='tipo',
            field=models.CharField(default=django.utils.timezone.now, max_length=15),
            preserve_default=False,
        ),
    ]
