import io
import zipfile
from pathlib import Path

from bokeh.client import pull_session
from bokeh.embed import server_session
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django_dicom.models import Series
from django_mri.filters.scan_filter import ScanFilter
from django_mri.models import Scan
from django_mri.serializers import ScanSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.views.utils import fix_bokeh_script
from nilearn.plotting.html_document import HTMLDocument
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

HOST_NAME = getattr(settings, "APP_IP", "localhost")
BOKEH_URL = f"http://{HOST_NAME}:5006/series_viewer"
CONTENT_DISPOSITION = "attachment; filename={instance_id}.zip"
ZIP_CONTENT_TYPE = "application/x-zip-compressed"


class ScanViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Scan.objects.order_by("-time__date", "time__time")
    serializer_class = ScanSerializer
    filter_class = ScanFilter
    search_fields = (
        "id",
        "description",
        "number",
        "created",
        "scan_time",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "sequence_type",
        "spatial_resolution",
        "institution_name",
        "is_updated_from_dicom",
    )
    ordering_fields = (
        "id",
        "time__date",
        "time__time",
        "description",
        "number",
        "created",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "sequence_type",
        "spatial_resolution",
        "institution_name",
    )

    def get_queryset(self) -> QuerySet:
        """
        Filter the returned scans according to the studies the requesting
        user is a collaborator in, unless the user is staff, in which case
        return all scans.

        Returns
        -------
        QuerySet
            Scan instances.
        """

        user = get_user_model().objects.get(username=self.request.user)
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return queryset.filter(study_groups__study__collaborators=user)

    # @action(detail=False, methods=["POST"])
    # def from_file(self, request):
    #     """
    #     Creates a new scan instance from a file (currently only DICOM format
    #     files are accepted).

    #     Parameters
    #     ----------
    #     request :
    #         A request from the client.

    #     Returns
    #     -------
    #     Response
    #         A response containing the serialized data or a message.
    #     """
    #     file_obj = request.data["file"]
    #     subject = get_subject_model().objects.get(
    #                   id=request.data["subject_id"]
    #               )
    #     user = get_user_model().objects.get(username=self.request.user)

    #     if file_obj.name.endswith(".dcm"):
    #         scan, created = ImportScan(
    #             subject, file_obj, scan_type="dcm", user=user
    #         ).run()
    #         serializer = ScanSerializer(scan, context={"request": request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     elif file_obj.name.endswith(".zip"):
    #         content = ContentFile(file_obj.read())
    #         temp_file_name = default_storage.save("tmp.zip", content)
    #         temp_file_path = os.path.join(
    #                              settings.MEDIA_ROOT, temp_file_name
    #                              )
    #         LocalImport(subject, temp_file_path, user=user).run()
    #         os.remove(temp_file_path)
    #         return Response(
    #             {"message": "Successfully imported ZIP archive!"},
    #             status=status.HTTP_201_CREATED,
    #         )

    @action(detail=True, methods=["GET"])
    def from_dicom(self, request: Request, series_id: int = None) -> Response:
        """
        Returns scan information from a
        :class:`~django_dicom.models.series.Series` instance without
        serializing.

        Parameters
        ----------
        request :
            A request from the client.
        series_id : int, optional
            :class:`~django_dicom.models.series.Series` primary key, by
            default None

        Returns
        -------
        Response
            Serialized data or messagerequirements
        """
        try:
            series = Series.objects.get(id=series_id)
        except ObjectDoesNotExist:
            return Response(
                "Invalid DICOM primary key!",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            scan = Scan.objects.get(dicom=series)
            res = ScanSerializer(data=scan, context={"request": request})
            res.is_valid()
            return Response(res.validated_data)
        except ObjectDoesNotExist:
            scan = Scan(dicom=series)
            scan.update_fields_from_dicom()
            serializer = ScanSerializer(scan, context={"request": request})
            return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def plot(self, request: Request, pk: int = None) -> Response:
        arguments = {"scan_id": str(pk)}
        with pull_session(url=BOKEH_URL, arguments=arguments) as session:
            script = server_session(session_id=session.id, url=BOKEH_URL)
        return Response(script)

    @action(detail=True, methods=["GET"])
    def preview_script(self, request: Request, pk: int = None) -> Response:
        arguments = {"scan_id": str(pk)}
        destination_id = request.GET.get("elementId", "bk-plot")
        with pull_session(url=BOKEH_URL, arguments=arguments) as session:
            html = server_session(session_id=session.id, url=BOKEH_URL)
            script = fix_bokeh_script(html, destination_id=destination_id)
        return HttpResponse(script, content_type="text/javascript")

    @action(detail=True, methods=["GET"])
    def nilearn_plot(self, request: Request, pk: int = None) -> Response:
        scan = Scan.objects.get(id=pk)
        try:
            content = scan.html_plot()
        except RuntimeError as e:
            content = f"Failed to generate scan preview with the following exception:\n{e}"
        else:
            if isinstance(content, HTMLDocument):
                content = content.get_iframe(width=1000, height=500)
        return JsonResponse({"content": content})

    @action(detail=True, methods=["get"])
    def nifti_zip(self, request: Request, pk: int) -> HttpResponse:
        instance = Scan.objects.get(id=pk)
        try:
            nii_path = Path(instance.nifti.path)
        except (AttributeError, RuntimeError):
            return HttpResponse(
                f"Could not create NIfTI format version of scan #{pk}"
            )
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            nii_name = nii_path.name
            zip_file.write(nii_path, nii_name)
            json_file = Path(instance.nifti.json_file)
            if json_file.exists():
                zip_file.write(json_file, json_file.name)
        response = HttpResponse(
            buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
        )
        content_disposition = CONTENT_DISPOSITION.format(instance_id=pk)
        response["Content-Disposition"] = content_disposition
        return response

    @action(detail=False, methods=["get"])
    def listed_nifti_zip(
        self, request: Request, scan_ids: str
    ) -> HttpResponse:
        scan_ids = [int(pk) for pk in scan_ids.split(",")]
        queryset = Scan.objects.filter(id__in=scan_ids)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            for instance in queryset:
                try:
                    nii_path = Path(instance.nifti.path)
                except (AttributeError, RuntimeError):
                    return HttpResponse(
                        f"Could not create NIfTI format version of scan #{instance.id}"
                    )
                nii_name = nii_path.name
                zip_file.write(nii_path, nii_name)
                json_file = Path(instance.nifti.json_file)
                if json_file.exists():
                    zip_file.write(json_file, json_file.name)
        response = HttpResponse(
            buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
        )
        content_disposition = CONTENT_DISPOSITION.format(instance_id="scans")
        response["Content-Disposition"] = content_disposition
        return response
