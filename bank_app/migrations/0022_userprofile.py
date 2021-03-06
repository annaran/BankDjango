# Generated by Django 3.1.2 on 2020-10-29 21:50

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0021_auto_20201029_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('user_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank_app.bank_acccount')),
            ],
        ),
    ]
