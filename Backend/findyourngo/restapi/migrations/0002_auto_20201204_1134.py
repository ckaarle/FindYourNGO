# Generated by Django 3.1.3 on 2020-12-04 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngotwscore',
            name='credible_source_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ngotwscore',
            name='ecosoc_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ngotwscore',
            name='number_data_sources_score',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='ngotwscore',
            name='total_tw_score',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
