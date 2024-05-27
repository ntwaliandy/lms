# Generated by Django 4.0.5 on 2024-05-26 08:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0020_bodaapply_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_id', models.CharField(default='null', max_length=200)),
                ('expenditures', models.DecimalField(decimal_places=2, default='0', max_digits=20)),
                ('collections', models.DecimalField(decimal_places=2, default='0', max_digits=20)),
                ('banked_balance', models.DecimalField(decimal_places=2, default='0', max_digits=20)),
                ('note', models.TextField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]