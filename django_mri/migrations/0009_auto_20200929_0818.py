# Generated by Django 3.0.8 on 2020-09-29 08:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_mri", "0008_auto_20200827_0229"),
        migrations.swappable_dependency(settings.MEASUREMENT_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="measurement",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mri_session_set",
                to=settings.MEASUREMENT_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="session", name="time", field=models.DateTimeField(),
        ),
    ]
