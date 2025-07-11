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

    field_handlers = {
        'username': handle_username_errors,
        'password': handle_password_errors,
        'email': handle_email_errors,
        'refresh': handle_refresh_errors,
        #'title': handle_title_errors,
        #'route': handle_route_errors,
        #'media': handle_media_errors,
        #'start_date': handle_start_date_errors,
        #'end_date': handle_end_date_errors,
    }

    for field, handler in field_handlers.items():
        if field in data:
            return handler(data[field])

    return {
        "message": MessagesES.GENERIC_VALIDATION_ERROR,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_username_errors(errors):

    first_error = str(errors[0])

    if first_error == MessagesES.ERROR_USER_ALREADY_EXISTS:
        return {
            "message": MessagesES.ERROR_USER_ALREADY_EXISTS,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif first_error == MessagesES.ERROR_USERNAME_TYPE:
        return {
            "message": MessagesES.ERROR_USERNAME_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }

    return {
        "message": MessagesES.ERROR_USERNAME_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_password_errors(errors):
    return {
        "message": MessagesES.ERROR_PASSWORD_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_email_errors(errors):
    
    first_error = str(errors[0])

    if first_error == MessagesES.ERROR_EMAIL_ALREADY_EXISTS:
        return {
            "message": MessagesES.ERROR_EMAIL_ALREADY_EXISTS,
            "status": status.HTTP_400_BAD_REQUEST
        }

    return {
        "message": MessagesES.ERROR_EMAIL_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_refresh_errors(errors):
    return {
        "message": MessagesES.ERROR_REFRESH_REQUIRED,
        "status": status.HTTP_401_UNAUTHORIZED
    }

# Mapa de excepciones
EXCEPTION_HANDLERS = {
    AuthenticationFailed: handle_authentication_failed,
    ValidationError: handle_validation_error,
}
