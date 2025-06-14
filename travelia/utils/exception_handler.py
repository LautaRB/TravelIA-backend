from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework import status
from .messeges import *
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Obtener el mensaje de error
        message = str(exc.__class__.__name__)

        if isinstance(exc, AuthenticationFailed):
            message = ERROR_BAD_CREDENTIALS

        elif isinstance(exc, ValidationError):
            if 'username' in response.data:
                message = ERROR_USERNAME_REQUIRED
            elif 'password' in response.data:
                message = ERROR_PASSWORD_REQUIRED
            elif 'email' in response.data:
                message = ERROR_EMAIL_REQUIRED
            else:
                message = "Datos inválidos"

        custom_response_data = {
            "error": True,
            "message": message,
            "details": response.data
        }
        response.data = custom_response_data

    else:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return Response(
            {
                "error": True,
                "message": "Error interno del servidor",
                "details": str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response