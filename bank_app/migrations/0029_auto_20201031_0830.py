# Generated by Django 3.1.2 on 2020-10-31 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0028_auto_20201030_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.CharField(default='standard', max_length=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='corresponding_account',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='no description', max_length=200),
        ),
    ]