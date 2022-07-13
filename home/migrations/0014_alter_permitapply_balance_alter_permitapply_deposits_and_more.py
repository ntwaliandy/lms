# Generated by Django 4.0.5 on 2022-07-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_permitapply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permitapply',
            name='balance',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12),
        ),
        migrations.AlterField(
            model_name='permitapply',
            name='deposits',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12),
        ),
        migrations.AlterField(
            model_name='permitapply',
            name='final_amount',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12),
        ),
    ]
