# Generated by Django 3.2.9 on 2021-12-04 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0006_lookupevent_lookupschedule_lookupscheduletype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lookupevent',
            name='ticker',
        ),
        migrations.AddField(
            model_name='lookupevent',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tradeklines',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tickers.lookupscheduletype'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='tradeklines',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='tradeklines',
            name='sequence',
        ),
    ]