# Generated by Django 3.1.5 on 2021-03-23 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0006_auto_20210323_0859'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donors',
            old_name='pincode',
            new_name='zipcode',
        ),
        migrations.RemoveField(
            model_name='donors',
            name='district',
        ),
        migrations.AddField(
            model_name='donors',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='donors',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
