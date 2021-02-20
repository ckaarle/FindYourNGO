# Generated by Django 3.1.6 on 2021-02-20 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0004_auto_20210220_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnconfirmedNgo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.ngocountry')),
                ('meta_data', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restapi.ngometadata')),
                ('representative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.ngorepresentative')),
            ],
        ),
    ]
