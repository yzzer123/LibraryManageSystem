# Generated by Django 3.0.3 on 2020-05-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0023_auto_20200517_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='isLegal',
            field=models.NullBooleanField(default=True),
        ),
    ]
