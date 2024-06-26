# Generated by Django 3.1.2 on 2024-05-15 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='noname', max_length=30)),
                ('owner', models.CharField(max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='flight.place')),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('1', 'premium'), ('2', 'deluxe'), ('3', 'basic')], max_length=50)),
                ('capacity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('size', models.IntegerField()),
                ('status', models.CharField(choices=[('1', 'available'), ('2', 'not available')], max_length=15)),
                ('room_number', models.IntegerField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotels')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('booking_id', models.CharField(default='null', max_length=100)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.rooms')),
            ],
        ),
    ]
