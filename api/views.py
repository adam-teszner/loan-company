import os
import tempfile
import zipfile
from collections import OrderedDict

from django.conf import settings
from django.http.response import FileResponse, HttpResponse
from django.utils.encoding import force_str
from rest_framework import exceptions, serializers, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.field_mapping import ClassLookupDict

from api.pdfgen import create_product_detail_pdf
from core.models import Customer, Product
from .serializers import (CustomerSerializer, PDFProductSeriaziler,
                          ProductSerializer)


class CustomerUpdateFetchApiView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    '''
    Class for updating Customer details using JS fetch().
    -----
    Some parts are copied from rest_frameworks metadata class, to generate
    custom json schema -> so the front-end JS function are able to create
    forms and with choice fields etc.
    -----
    '''

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    metadata_class = None

    # Specifies which fields to serialize on GET request
    field_params = {
        "basic": [
            "first_name",
            "last_name",
            "gender",
            "dob",
            "martial_status",
            "social_security_no_pesel",
            "id_passport",
        ],
        "contact": [
            "adress",
            "phone_no",
            "email",
        ],
        "workplace": [
            "work_status",
            "workplace",
            "position",
            "salaty",
            "esd",
        ],
    }

    label_lookup = ClassLookupDict(
        {
            serializers.Field: "field",
            serializers.BooleanField: "boolean",
            serializers.CharField: "string",
            serializers.UUIDField: "string",
            serializers.URLField: "url",
            serializers.EmailField: "email",
            serializers.RegexField: "regex",
            serializers.SlugField: "slug",
            serializers.IntegerField: "integer",
            serializers.FloatField: "float",
            serializers.DecimalField: "decimal",
            serializers.DateField: "date",
            serializers.DateTimeField: "datetime",
            serializers.TimeField: "time",
            serializers.ChoiceField: "choice",
            serializers.MultipleChoiceField: "multiple choice",
            serializers.FileField: "file upload",
            serializers.ImageField: "image upload",
            serializers.ListField: "list",
            serializers.DictField: "nested object",
            serializers.Serializer: "nested object",
        }
    )

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        instance = Customer.objects.get(pk=pk)
        mode = request.query_params.get("mode", default=None)

        data = {}
        data["initial"] = CustomerSerializer(
            instance=instance, fields=self.field_params[mode]
        ).data
        schema = self.get_serializer_info(self.get_serializer())
        filtered_data = {}
        for k in self.field_params[mode]:
            filtered_data[k] = schema.pop(k)
        data["schema"] = filtered_data
        if request.user.id != instance.created_by.id:
            raise exceptions.PermissionDenied
        return Response(data)

    def get_serializer_info(self, serializer):
        """
        Given an instance of a serializer, return a dictionary of metadata
        about its fields.
        """
        if hasattr(serializer, "child"):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return OrderedDict(
            [
                (field_name, self.get_field_info(field))
                for field_name, field in serializer.fields.items()
                if not isinstance(field, serializers.HiddenField)
            ]
        )

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        field_info["type"] = self.label_lookup[field]
        field_info["required"] = getattr(field, "required", False)

        attrs = [
            "read_only",
            "label",
            "help_text",
            "min_length",
            "max_length",
            "min_value",
            "max_value",
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != "":
                # field_info[attr] = force_str(value, strings_only=True)
                field_info[attr] = force_str(value, strings_only=True)

        if getattr(field, "child", None):
            field_info["child"] = self.get_field_info(field.child)
        elif getattr(field, "fields", None):
            field_info["children"] = self.get_serializer_info(field)

        if (
            not field_info.get("read_only")
            and not isinstance(
                field, (serializers.RelatedField, serializers.ManyRelatedField)
            )
            and hasattr(field, "choices")
        ):
            field_info["choices"] = [
                {
                    "value": choice_value,
                    "display_name": force_str(choice_name, strings_only=True),
                }
                for choice_value, choice_name in field.choices.items()
            ]

        return field_info

    def put(self, *args, **kwargs):
        return self.partial_update(self.request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Limiting edit/save/create access for "guest_user"
        if request.user.username == "guest":
            raise exceptions.PermissionDenied

        instance = Customer.objects.get(pk=kwargs["pk"])
        mode = request.query_params.get("mode", default=None)
        serializer = self.get_serializer(
            instance=instance,
            data=self.request.data,
            partial=True,
            fields=self.field_params[mode],
        )

        if request.user.id != instance.created_by.id:
            raise exceptions.PermissionDenied

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class SearchApiView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        allowed_params = [
            "id",
            "owner__first_name",
            "owner__last_name",
            "owner__social_security_no_pesel",
            "owner__adress__city",
            "owner__adress__zip_code",
            "owner__workplace__name",
            "owner__workplace__id_nip",
            "owner__work_status",
            "amount_requested__lte",
            "amount_requested__gte",
            "tot_paid__gte",
            "tot_paid__lte",
            "tot_amout__gte",
            "tot_amout__lte",
            "tot_debt__gte",
            "tot_debt__lte",
            "tot_delay__gte",
            "tot_delay__lte",
            "created_date__gte",
            "created_date__lte",
        ]

        params = {
            k: v for (k, v) in self.request.query_params.items() if k in allowed_params
        }
        if self.request.query_params.get("sadb"):
            return Product.objects.filter(**params).order_by("id")

        return (
            Product.objects.filter(
                owner__created_by__userinfo__user__id=self.request.user.id
            )
            .filter(**params)
            .order_by("id")
        )


class GeneratePDFView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PDFProductSeriaziler
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Returns queryset of Product objects created by current user and
        filtered by specified list of id's.

        Id's are of Products selected by user.
        """
        qs = Product.objects.filter(
            owner__created_by__userinfo__user__id=self.request.user.id
        )
        query_params = self.request.query_params.get("id")
        id_list = query_params.split(",")
        return qs.filter(id__in=id_list)

    def list(self, *args, **kwargs):
        """
        Reposnds with single .pdf file if only one product is selected,
        or with .zip file (containing pdf's) if many produts are selected.

        Created files are stored in temp directory, so after closure, they
        are deleted.

        """
        files = []
        tmp_path = os.path.join(settings.MEDIA_ROOT, "pdf")
        os.makedirs(tmp_path, exist_ok=True)
        folder = tempfile.TemporaryDirectory(dir=tmp_path)

        # Basically data is the serializer.data of Product model
        data = super().list(*args, **kwargs)
        for prod in data.data.get("results"):
            files.append(create_product_detail_pdf(prod, folder))

        # Checks 'files' lenght to determine .pdf or .zip response
        if len(files) > 1:
            zip_path = os.path.join(tmp_path, folder.name, "doc.zip")
            with zipfile.ZipFile(zip_path, mode="w") as z:
                for path, fn in files:
                    file = os.path.join(path, fn)
                    z.write(file, arcname=file.rsplit("/")[-1])
            with open(zip_path, "rb") as zip_file:
                response = HttpResponse(
                    zip_file.read(),
                    content_type="application/x-zip-compressed"
                )
                response["Content-Disposition"] = "attachment; filename=doc.zip"
                return response
        file = os.path.join(files[0][0], files[0][1])
        return FileResponse(open(file, "rb"), as_attachment=True)
