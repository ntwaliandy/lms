# Generated by Django 4.0.5 on 2023-04-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0016_bodaweeklypay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodaweeklypay',
            name='transaction_id',
            field=models.CharField(default='null', max_length=200),
        ),
    ]