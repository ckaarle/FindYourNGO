# Generated by Django 3.1.4 on 2020-12-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20201204_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngotwscore',
            name='wce_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ngostats',
            name='member_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ngostats',
            name='staff_number',
            field=models.IntegerField(default=0),
        ),
    ]