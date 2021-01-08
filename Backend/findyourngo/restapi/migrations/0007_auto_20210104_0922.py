# Generated by Django 3.1.4 on 2021-01-04 09:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0006_auto_20201227_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='NgoReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField()),
                ('last_edited', models.DateField()),
                ('text', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.ngo')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.ngocommenter')),
            ],
        ),
        migrations.DeleteModel(
            name='NgoComment',
        ),
    ]
