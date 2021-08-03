from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.status import (
    HTTP_412_PRECONDITION_FAILED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """ overwrite custom exception """
    logger.error(''.join(traceback.format_exception(
        etype=type(exc), value=exc, tb=exc.__traceback__)))
    # current_url = str(context['request'].path).split('/')[1]
    response = exception_handler(exc, context)
    if response is not None:
        errors = {}
        for field, value in response.data.items():
            if isinstance(value, list):
                errors[f'{field}'] = f'{value[0]}'
        response.data = {"success": False}
        if hasattr(exc, 'detail'):
            response.data['errors'] = exc.detail
        if hasattr(exc, 'redirect'):
            response.data['redirect'] = exc.redirect
        if hasattr(exc, 'notifications'):
            notifications = exc.notifications
            if exc.notifications is None:
                notifications = []
            response.data['notifications'] = notifications
    return response


class ValidationException(APIException):
    status_code = HTTP_200_OK

    def __init__(self, detail={}):
        self.detail = detail


class CommonException(APIException):

    def __init__(self, status_code=HTTP_400_BAD_REQUEST, detail={}):
        self.status_code = status_code
        self.detail = detail


class NotFoundException(APIException):
    status_code = HTTP_404_NOT_FOUND

    def __init__(self, detail={}):
        self.detail = detail


class PreconditionFailedException(APIException):
    status_code = HTTP_412_PRECONDITION_FAILED

    def __init__(self, detail={}):
        self.detail = detail


class ForbiddenException(APIException):
    status_code = HTTP_403_FORBIDDEN

    def __init__(self, detail={}, redirect=None):
        self.detail = detail
        self.redirect = redirect
