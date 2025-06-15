from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework import status
from .messeges import MessagesES
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Obtener el mensaje de error
        message = str(exc.__class__.__name__)

        if isinstance(exc, AuthenticationFailed):
            message = MessagesES.ERROR_BAD_CREDENTIALS
            estado = status.HTTP_401_UNAUTHORIZED

        elif isinstance(exc, ValidationError):
            if 'username' in response.data:
                username_errors = response.data.get('username')
                if username_errors and isinstance(username_errors, list):
                    first_error_username = str(username_errors[0])
                
                if first_error_username == MessagesES.ERROR_USER_ALREADY_EXISTS:
                    message = MessagesES.ERROR_USER_ALREADY_EXISTS
                    estado = status.HTTP_400_BAD_REQUEST
                else:
                    message = MessagesES.ERROR_USERNAME_REQUIRED
                    estado = status.HTTP_400_BAD_REQUEST
            elif 'password' in response.data:
                message = MessagesES.ERROR_PASSWORD_REQUIRED
                estado = status.HTTP_400_BAD_REQUEST
            elif 'email' in response.data:
                email_errors = response.data.get('email')
                if email_errors and isinstance(email_errors,list):
                    first_error_email = str(email_errors[0])
                
                if first_error_email == MessagesES.ERROR_EMAIL_ALREADY_EXISTS:
                    message = MessagesES.ERROR_EMAIL_ALREADY_EXISTS
                    estado = status.HTTP_400_BAD_REQUEST
                else:
                    message = MessagesES.ERROR_EMAIL_REQUIRED
                    estado = status.HTTP_400_BAD_REQUEST
            else:
                message = "Datos inválidos"
                estado = status.HTTP_400_BAD_REQUEST

        custom_response_data = {
            "error": True,
            "status": estado,
            "message": message,
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