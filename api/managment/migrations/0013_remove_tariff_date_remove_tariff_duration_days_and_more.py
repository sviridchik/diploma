# Generated by Django 4.1.1 on 2023-05-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('managment', '0012_guardiansetting_patient_current'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='date',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='duration_days',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='user',
        ),
        migrations.AddField(
            model_name='tariff',
            name='title',
            field=models.CharField(default='title', max_length=100),
            preserve_default=False,
        ),
    ]
