# Generated by Django 3.0.3 on 2020-05-20 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0024_auto_20200517_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='FineMoney',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
