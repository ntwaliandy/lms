# Generated by Django 2.2.12 on 2022-02-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0005_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replies',
            name='question_id',
            field=models.IntegerField(),
        ),
    ]