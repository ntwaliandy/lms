# Generated by Django 3.0.5 on 2022-01-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='transction_id',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
