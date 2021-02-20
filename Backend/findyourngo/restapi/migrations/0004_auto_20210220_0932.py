# Generated by Django 3.1.6 on 2021-02-20 09:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_ngotwscore_ngo_account_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='NgoTWDataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_tw_score', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='ngotwscore',
            name='tw_series',
            field=models.ManyToManyField(to='restapi.NgoTWDataPoint'),
        ),
    ]
