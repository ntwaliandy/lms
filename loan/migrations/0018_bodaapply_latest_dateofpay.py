# Generated by Django 4.0.5 on 2023-04-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0017_alter_bodaweeklypay_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodaapply',
            name='latest_dateOfPay',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]