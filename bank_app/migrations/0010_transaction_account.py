# Generated by Django 3.1.2 on 2020-10-25 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0009_remove_transaction_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ManyToManyField(blank=True, null=True, to='bank_app.Bank_acccount'),
        ),
    ]
