from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .messeges import MessagesES
from rest_framework import status

def handle_authentication_failed(exc, response):
    return {
        "message": MessagesES.ERROR_BAD_CREDENTIALS,
        "status": status.HTTP_401_UNAUTHORIZED
    }

def handle_validation_error(exc, response):
    data = response.data
    
    if 'username' in data:
        username_errors = data.get('username')
        if username_errors:
            first_error_username = str(username_errors[0]) if username_errors else ''
            if first_error_username == MessagesES.ERROR_USER_ALREADY_EXISTS:
                return {
                    "message": MessagesES.ERROR_USER_ALREADY_EXISTS,
                    "status": status.HTTP_400_BAD_REQUEST
                }
        return {
            "message": MessagesES.ERROR_USERNAME_REQUIRED,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif 'password' in data:
        return {
            "message": MessagesES.ERROR_PASSWORD_REQUIRED,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif 'email' in data:
        email_errors = data.get('email')
        if email_errors:
            first_error_email = str(email_errors[0]) if email_errors else ''
            if first_error_email == MessagesES.ERROR_EMAIL_ALREADY_EXISTS:
                return {
                    "message": MessagesES.ERROR_EMAIL_ALREADY_EXISTS,
                    "status": status.HTTP_400_BAD_REQUEST
                }
        return {
            "message": MessagesES.ERROR_EMAIL_REQUIRED,
            "status": status.HTTP_400_BAD_REQUEST
        }
    return {
        "message": "Datos inválidos",
        "status": status.HTTP_400_BAD_REQUEST
    }

# Mapa de excepciones
EXCEPTION_HANDLERS = {
    AuthenticationFailed: handle_authentication_failed,
    ValidationError: handle_validation_error,
}
