# Generated by Django 3.0.3 on 2020-05-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0022_borrow_realreturnday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='LimitDay',
            field=models.PositiveSmallIntegerField(db_index=True, unique=True),
        ),
    ]
