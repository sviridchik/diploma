# Generated by Django 3.2.16 on 2022-11-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_alter_schedule_strict_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='schedule',
        ),
        migrations.AddField(
            model_name='schedule',
            name='timesheet',
            field=models.ManyToManyField(to='medicine.TimeTable', verbose_name='time'),
        ),
    ]
