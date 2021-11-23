"""
Definition of the :class:`Session` class.
"""
from pathlib import Path
from typing import List

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_mri.models import help_text
from django_mri.models.managers.session import SessionQuerySet
from django_mri.utils import (
    get_group_model,
    get_measurement_model,
    get_study_model,
    get_subject_model,
)

Group = get_group_model()
MeasurementDefinition = get_measurement_model()
Study = get_study_model()
Subject = get_subject_model()

SECONDS_IN_YEAR: int = 60 * 60 * 24 * 365
CLAIMED_SESSION_STRING: str = "Subject #{subject_id} MRI session from {date}"
UNCLAIMED_SESSION_STRING: str = "Unclaimed MRI session from {date}"
DICOM_FILES_KEY: str = "dicom__image__dcm"
NIFTI_FILES_KEY: str = "_nifti__path"


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: The associated `Subject` model (optional).
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="mri_session_set",
        blank=True,
        null=True,
    )

    #: Any other information about this scanning sequence.
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=help_text.SESSION_COMMENTS,
    )

    #: The associated `Measurement` model (optional).
    measurement = models.ForeignKey(
        MeasurementDefinition,
        related_name="mri_session_set",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    #: The date and time in which this scanning sequence began.
    time = models.DateTimeField()

    #: Associated IRB approval.
    irb = models.ForeignKey(
        "django_mri.IrbApproval",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="IRB approval",
    )

    objects = SessionQuerySet.as_manager()

    class Meta:
        ordering = ("-time",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        date = self.time.date()
        if self.subject:
            return CLAIMED_SESSION_STRING.format(
                subject_id=self.subject.id, date=date
            )
        return UNCLAIMED_SESSION_STRING.format(date=date)

    def infer_subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the session
        acquisition. If the subject's date of birth or the session's
        acquisition time are not available, returns `None`.

        See Also
        --------
        * :func:`subject_age`

        Returns
        -------
        float
            Subject age in years at the time of the session's acquisition
        """
        has_required_info = (
            self.time and self.subject and self.subject.date_of_birth
        )
        if has_required_info:
            delta = self.time.date() - self.subject.date_of_birth
            return delta.total_seconds() / SECONDS_IN_YEAR

    def list_dicom_files(self) -> List[Path]:
        """
        Returns a list of the *.dcm* paths that make up the entire raw session
        data.

        Returns
        -------
        List[Path]
            *.dcm* files
        """
        return [
            Path(p)
            for p in self.scan_set.values_list(DICOM_FILES_KEY, flat=True)
        ]

    def list_nifti_files(self) -> List[Path]:
        """
        Returns a list of *.nii* files (and by default also JSON sidecars)
        included in this session.

        Returns
        -------
        List[Path]
            *.nii* files
        """
        paths = []
        for scan in self.scan_set.all(_nifti__isnull=False):
            nii_paths = scan.nifti.get_file_paths()
            paths += nii_paths
        return paths

    def query_measurement_studies(self) -> models.QuerySet:
        if self.measurement:
            return Study.objects.filter(
                id__in=self.measurement.procedure_set.values("study")
            )
        return Study.objects.none()

    def query_study_groups(self) -> models.QuerySet:
        return Group.objects.filter(
            id__in=self.scan_set.values("study_groups")
        )

    def query_studies(self) -> models.QuerySet:
        return self.query_measurement_studies() | Study.objects.filter(
            id__in=self.study_groups.values("study__id")
        )

    @property
    def subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the session
        acquisition. If the subject's date of birth or the session's
        acquisition time are not available, returns `None`.

        See Also
        --------
        * :func:`infer_subject_age`

        Returns
        -------
        float
            Subject age in years at the time of the session's acquisition
        """
        return self.infer_subject_age()

    @property
    def study_groups(self) -> models.QuerySet:
        """
        Returns a queryset of associated :class:`~research.models.group.Group`
        instances.

        Returns
        -------
        models.QuerySet
            Associated study groups
        """
        return self.query_study_groups()
