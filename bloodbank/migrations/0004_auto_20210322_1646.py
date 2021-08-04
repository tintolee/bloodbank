# Generated by Django 3.1.5 on 2021-03-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0003_auto_20210226_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brequests',
            name='attendant_name',
        ),
        migrations.RemoveField(
            model_name='brequests',
            name='contact_number',
        ),
        migrations.AddField(
            model_name='brequests',
            name='attendantname',
            field=models.CharField(default=100, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brequests',
            name='contactnumber',
            field=models.CharField(default=15, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brequests',
            name='state',
            field=models.CharField(default=100, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brequests',
            name='town',
            field=models.CharField(default=100, max_length=50),
            preserve_default=False,
        ),
    ]
