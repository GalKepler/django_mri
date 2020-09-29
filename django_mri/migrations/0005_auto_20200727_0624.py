# Generated by Django 3.0.6 on 2020-07-27 06:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_mri", "0004_auto_20200722_0026"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scan",
            name="echo_time",
            field=models.FloatField(
                blank=True,
                help_text="The time between the application of the radio-frequency excitation pulse and the peak of the signal induced in the coil (in milliseconds).",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
