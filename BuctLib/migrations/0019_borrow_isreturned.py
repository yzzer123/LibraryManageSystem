# Generated by Django 3.0.3 on 2020-05-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0018_auto_20200514_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='isReturned',
            field=models.BooleanField(default=False),
        ),
    ]
