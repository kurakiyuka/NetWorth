# Generated by Django 2.2.6 on 2019-11-07 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0009_currencytype_update_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='netmodel',
            old_name='currency_type',
            new_name='currencytype'
        ),
        migrations.AlterField(
            model_name='currencytype',
            name='currency_type_name',
            field=models.CharField(choices=[('RMB', '人民币'), ('HKD', '港元'), ('USD', '美元')], default='RMB', max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='MonthlyChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_name', models.CharField(max_length=20)),
                ('total_price', models.FloatField(default=0.0)),
                ('changed_price', models.FloatField(default=0.0)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('change_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='net.NetModel')),
            ],
        ),
    ]