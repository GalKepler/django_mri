# Generated by Django 3.0.6 on 2020-07-02 02:47

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_mri.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("django_dicom", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.SUBJECT_MODEL),
        migrations.swappable_dependency(settings.STUDY_GROUP_MODEL),
        ("django_analyses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NIfTI",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("path", models.FilePathField(max_length=1000, unique=True)),
                ("is_raw", models.BooleanField(default=False)),
            ],
            options={"verbose_name": "NIfTI",},
        ),
        migrations.CreateModel(
            name="NiftiInputDefinition",
            fields=[
                (
                    "inputdefinition_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.InputDefinition",
                    ),
                ),
            ],
            bases=("django_analyses.inputdefinition",),
        ),
        migrations.CreateModel(
            name="NiftiOutputDefinition",
            fields=[
                (
                    "outputdefinition_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.OutputDefinition",
                    ),
                ),
            ],
            bases=("django_analyses.outputdefinition",),
        ),
        migrations.CreateModel(
            name="Scan",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "institution_name",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "time",
                    models.DateTimeField(
                        blank=True,
                        help_text="The time in which the scan was acquired.",
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="A short description of the scan's acqusition parameters.",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "number",
                    models.IntegerField(
                        blank=True,
                        help_text="The number of this scan relative to the session in which it was acquired.",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    "echo_time",
                    models.FloatField(
                        blank=True,
                        help_text="The time between the application of the radiofrequency excitation pulse and the peak of the signal induced in the coil (in milliseconds).",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    "repetition_time",
                    models.FloatField(
                        blank=True,
                        help_text="The time between two successive RF pulses (in milliseconds).",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    "inversion_time",
                    models.FloatField(
                        blank=True,
                        help_text="The time between the 180-degree inversion pulse and the following spin-echo (SE) sequence (in milliseconds).",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    "spatial_resolution",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(),
                        blank=True,
                        null=True,
                        size=3,
                    ),
                ),
                (
                    "comments",
                    models.TextField(
                        blank=True,
                        help_text="If anything noteworthy happened during acquisition, it may be noted here.",
                        max_length=1000,
                        null=True,
                    ),
                ),
                ("is_updated_from_dicom", models.BooleanField(default=False)),
                (
                    "_nifti",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="django_mri.NIfTI",
                    ),
                ),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mri_uploads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dicom",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scan",
                        to="django_dicom.Series",
                        verbose_name="DICOM Series",
                    ),
                ),
                (
                    "study_groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="mri_scans",
                        to=settings.STUDY_GROUP_MODEL,
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="mri_scans",
                        to=settings.SUBJECT_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "MRI Scans",},
        ),
        migrations.CreateModel(
            name="ScanInputDefinition",
            fields=[
                (
                    "inputdefinition_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.InputDefinition",
                    ),
                ),
            ],
            bases=("django_analyses.inputdefinition",),
        ),
        migrations.CreateModel(
            name="SequenceType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="title"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="description"
                    ),
                ),
                (
                    "scanning_sequence",
                    django_mri.models.fields.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("SE", "Spin Echo"),
                                ("IR", "Inversion Recovery"),
                                ("GR", "Gradient Recalled"),
                                ("EP", "Echo Planar"),
                                ("RM", "Research Mode"),
                            ],
                            max_length=2,
                        ),
                        blank=True,
                        null=True,
                        size=5,
                    ),
                ),
                (
                    "sequence_variant",
                    django_mri.models.fields.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("SK", "Segmented k-Space"),
                                ("MTC", "Magnetization Transfer Contrast"),
                                ("SS", "Steady State"),
                                ("TRSS", "Time Reversed Steady State"),
                                ("SP", "Spoiled"),
                                ("MP", "MAG Prepared"),
                                ("OSP", "Oversampling Phase"),
                                ("NONE", "None"),
                            ],
                            max_length=4,
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
            ],
            options={
                "ordering": ("title",),
                "unique_together": {("scanning_sequence", "sequence_variant")},
            },
        ),
        migrations.CreateModel(
            name="ScanInput",
            fields=[
                (
                    "input_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.Input",
                    ),
                ),
                (
                    "definition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="input_set",
                        to="django_mri.ScanInputDefinition",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="run_input_set",
                        to="django_mri.Scan",
                    ),
                ),
            ],
            bases=("django_analyses.input",),
        ),
        migrations.CreateModel(
            name="NiftiOutput",
            fields=[
                (
                    "output_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.Output",
                    ),
                ),
                (
                    "definition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="output_set",
                        to="django_mri.NiftiOutputDefinition",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="run_output_set",
                        to="django_mri.NIfTI",
                    ),
                ),
            ],
            bases=("django_analyses.output",),
        ),
        migrations.CreateModel(
            name="NiftiInput",
            fields=[
                (
                    "input_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_analyses.Input",
                    ),
                ),
                (
                    "definition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="input_set",
                        to="django_mri.NiftiInputDefinition",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="run_input_set",
                        to="django_mri.NIfTI",
                    ),
                ),
            ],
            bases=("django_analyses.input",),
        ),
    ]
