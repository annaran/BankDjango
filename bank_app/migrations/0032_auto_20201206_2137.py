# Generated by Django 3.1.2 on 2020-12-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0031_auto_20201206_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='a6d0dab2-93d3-44b8-ab9f-7c405d70cbdc', max_length=36),
        ),
    ]
