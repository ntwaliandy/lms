# Generated by Django 4.0.5 on 2023-04-19 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0015_alter_bodaapply_boda_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodaWeeklyPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boda_id', models.CharField(default='null', max_length=200)),
                ('boda_firstName', models.CharField(default='null', max_length=200)),
                ('boda_lastName', models.CharField(default='null', max_length=200)),
                ('payment_fee', models.DecimalField(decimal_places=2, default='0', max_digits=20)),
                ('phone_number', models.CharField(default='null', max_length=20)),
                ('transaction_id', models.CharField(default='null', max_length=200, unique=True)),
                ('status', models.CharField(default='null', max_length=200)),
                ('reference', models.CharField(default='null', max_length=200)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
