# Generated by Django 3.1.2 on 2024-05-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_auto_20240506_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(default='', upload_to='flight/static/car/images'),
        ),
    ]