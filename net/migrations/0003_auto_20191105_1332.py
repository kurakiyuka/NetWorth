# Generated by Django 2.2.6 on 2019-11-05 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0002_auto_20191105_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modifymodel',
            old_name='name',
            new_name='assets_name',
        ),
    ]
