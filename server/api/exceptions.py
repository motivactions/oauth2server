from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler
from django.core.exceptions import NON_FIELD_ERRORS as DJ_NON_FIELD_ERRORS
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import api_settings

DRF_NON_FIELD_ERRORS = api_settings.NON_FIELD_ERRORS_KEY


class APIServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Internal Server Error.")
    default_code = "server_error"


def error_handler(exc, context):
    # translate django validation error which ...
    # .. causes HTTP 500 status ==> DRF validation which will cause 400 HTTP status
    if isinstance(exc, DjangoValidationError):
        data = exc.message_dict
        if DJ_NON_FIELD_ERRORS in data:
            data[DRF_NON_FIELD_ERRORS] = data[DJ_NON_FIELD_ERRORS]
            del data[DJ_NON_FIELD_ERRORS]

        exc = DRFValidationError(detail=data)
    if isinstance(exc, (AttributeError,)):
        data = exc
        exc = APIServerError(detail=data)

    return drf_exception_handler(exc, context)
