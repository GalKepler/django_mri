"""
Definition of the app's models_.

.. _models:
   https://docs.djangoproject.com/en/3.0/topics/db/models/
"""

from django_mri.models.data_directory import DataDirectory
from django_mri.models.inputs.nifti_input import NiftiInput
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input import ScanInput
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from django_mri.models.irb_approval import IrbApproval
from django_mri.models.nifti import NIfTI
from django_mri.models.outputs.nifti_output import NiftiOutput
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)
from django_mri.models.scan import Scan
from django_mri.models.session import Session

# flake8: noqa: F401
