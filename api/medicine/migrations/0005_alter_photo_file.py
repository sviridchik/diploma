# Generated by Django 4.1.1 on 2023-05-24 06:33


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
