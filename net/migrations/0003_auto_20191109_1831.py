# Generated by Django 2.2.6 on 2019-11-09 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0002_auto_20191109_1829'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TotalNetModel',
            new_name='NetWorth',
        ),
    ]