# Generated by Django 4.2.4 on 2025-08-02 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='registration_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
