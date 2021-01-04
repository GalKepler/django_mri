"""
Definition of the :class:`Session` class.
"""

from django.db import models
from django.db.models import QuerySet
from django_extensions.db.models import TimeStampedModel
from django_mri.utils import (
    get_subject_model,
    get_group_model,
    get_measurement_model,
)
from django_mri.models import help_text
from django_mri.models.managers.session import SessionQuerySet

Group = get_group_model()


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: The associated `Subject` model (optional).
    subject = models.ForeignKey(
        get_subject_model(),
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
        get_measurement_model(),
        related_name="mri_session_set",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    #: The date and time in which this scanning sequence began.
    time = models.DateTimeField()

    #: Associated IRB approval.
    irb = models.ForeignKey(
        "django_mri.IrbApproval", on_delete=models.SET_NULL, null=True
    )

    objects = SessionQuerySet.as_manager()

    class Meta:
        ordering = ("-time",)

    @property
    def study_groups(self) -> QuerySet:
        """
        The experimental groups with which scans in this session are
        associated. This property is only relevant if `STUDY_GROUP_MODEL` is
        set in the project's settings.

        Returns
        -------
        QuerySet
            The associated study groups
        """

        ids = self.scan_set.values_list("study_groups", flat=True)
        return Group.objects.filter(id__in=ids)
