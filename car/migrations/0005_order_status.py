# Generated by Django 3.1.2 on 2024-05-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0004_auto_20240506_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('ENDED', 'Ended')], default='PENDING', max_length=45),
        ),
    ]
