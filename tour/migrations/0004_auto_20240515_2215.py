# Generated by Django 3.1.2 on 2024-05-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_auto_20240515_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]