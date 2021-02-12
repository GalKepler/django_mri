from datetime import datetime

import factory
import pytz
from django.db.models import signals
from django.test import TestCase
from django_analyses.models import AnalysisVersion, Run
from django_dicom.models import Image, Series
from django_mri import serializers
from django_mri.models import Scan, Session
from django_mri.models.inputs import ScanInput, ScanInputDefinition
from django_mri.serializers.input import ScanInputSerializer
from django_mri.serializers.input.scan_input_definition import \
    ScanInputDefinitionSerializer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from tests.fixtures import SIEMENS_DWI_SERIES_PATH
from tests.models import Subject


class ScanInputModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        series = Series.objects.first()
        subject, _ = Subject.objects.from_dicom_patient(series.patient)
        header = series.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session = Session.objects.create(subject=subject, time=session_time)
        cls.scan = Scan.objects.create(dicom=series, session=session)
        cls.definition = ScanInputDefinition.objects.create(key="test")
        version = AnalysisVersion.objects.create(
            title="TestVersion", description="desc"
        )
        run = Run.objects.create(analysis_version=version)
        cls.input = ScanInput.objects.create(
            value=cls.scan, definition=cls.definition, run=run
        )

    def setUp(self):
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.scan_serializer = serializers.ScanSerializer(
            instance=self.scan, context={"request": req}
        )
        self.input_serializer = ScanInputSerializer(
            instance=self.input, context={"request": req}
        )
        if not self.scan:
            self.fail("Test scan not created! Check signals.")

    def test_serializer(self):
        expected = {
            "id": self.input.id,
            "key": self.definition.key,
            "value": self.scan_serializer.data["id"],
            "run": Run.objects.last().id,
            "definition": self.definition.id,
        }
        result = self.input_serializer.data
        self.assertDictEqual(result, expected)


class ScanInputDefinitionModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        ScanInputDefinition.objects.create(key="test")

    def setUp(self):
        self.definition = ScanInputDefinition.objects.last()
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.definition_serializer = ScanInputDefinitionSerializer(
            instance=self.definition, context={"request": req}
        )

    def test_definition_serializer(self):
        expected = {
            "id": self.definition.id,
            "key": self.definition.key,
            "required": self.definition.required,
            "description": self.definition.description,
            "is_configuration": self.definition.is_configuration,
            "value_attribute": self.definition.value_attribute,
            "db_value_preprocessing": self.definition.db_value_preprocessing,
            "run_method_input": self.definition.run_method_input,
            "db_value_preprocessing": self.definition.db_value_preprocessing,
        }
        result = self.definition_serializer.data
        self.assertDictEqual(result, expected)
