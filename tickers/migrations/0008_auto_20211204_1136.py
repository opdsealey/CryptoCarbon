# Generated by Django 3.2.9 on 2021-12-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickers", "0007_auto_20211204_1134"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tradeklines",
            name="type",
        ),
        migrations.AddField(
            model_name="tradeklines",
            name="end",
            field=models.DateTimeField(default="2021-12-04T11:37:13.940879"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tradeklines",
            name="start",
            field=models.DateTimeField(default="2021-12-04T11:37:13.940879"),
            preserve_default=False,
        ),
    ]
