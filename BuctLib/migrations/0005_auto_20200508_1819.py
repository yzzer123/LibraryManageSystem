# Generated by Django 3.0.3 on 2020-05-08 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuctLib', '0004_auto_20200507_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='BookID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuctLib.Book'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='ReaderID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuctLib.Reader'),
        ),
    ]
