# Generated by Django 4.0.5 on 2022-06-29 10:29

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20220613_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='loan_id',
            field=models.CharField(default=home.models.random_string, max_length=200),
        ),
        migrations.AlterField(
            model_name='groupapply',
            name='loan_id',
            field=models.CharField(default=home.models.random_string, max_length=200),
        ),
        migrations.AlterField(
            model_name='support',
            name='email',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='support',
            name='question',
            field=models.CharField(max_length=200),
        ),
    ]
