# Generated by Django 3.0.4 on 2020-03-12 15:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id_number',
            field=models.IntegerField(validators=[django.core.validators.MaxLengthValidator(14)]),
        ),
    ]