# Generated by Django 3.1.5 on 2021-01-25 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_ngofavourites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ngofavourites',
            old_name='favourite_ngos',
            new_name='favourite_ngo',
        ),
    ]
