# Generated by Django 3.1.2 on 2020-10-26 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0011_auto_20201026_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank_acccount',
            name='transactions',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bank_app.bank_acccount'),
        ),
    ]
