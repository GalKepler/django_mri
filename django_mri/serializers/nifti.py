"""
Definition of the :class:`~django_mri.serializers.nifti.NiftiSerializer` class.
"""

from rest_framework import serializers

from django_mri.models import NIfTI


class NiftiSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the :class:`~django_mri.models.nifti.NIfTI` model.
    """

    url = serializers.HyperlinkedIdentityField(view_name="mri:nifti-detail")

    class Meta:
        model = NIfTI
        exclude = ("path",)
