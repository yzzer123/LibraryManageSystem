# Generated by Django 3.0.3 on 2020-05-12 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0016_auto_20200512_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='Title',
            field=models.CharField(max_length=40),
        ),
    ]
