# Generated by Django 3.1.5 on 2021-03-31 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0011_auto_20210331_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact_us',
            old_name='state',
            new_name='email',
        ),
    ]