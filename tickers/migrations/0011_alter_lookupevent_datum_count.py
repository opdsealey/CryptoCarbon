# Generated by Django 3.2.9 on 2021-12-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0010_auto_20211204_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookupevent',
            name='datum_count',
            field=models.IntegerField(default=0),
        ),
    ]
