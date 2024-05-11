# Generated by Django 3.1.2 on 2024-05-07 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0005_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('CLOSED', 'Closed')], default='PENDING', max_length=45),
        ),
    ]