# Generated by Django 3.2.9 on 2021-12-03 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='maker_coefficient',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='maker_fee_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='symbol_name',
            field=models.CharField(default=1, max_length=24),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticker',
            name='taker_coefficient',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='taker_fee_rate',
            field=models.FloatField(null=True),
        ),
    ]