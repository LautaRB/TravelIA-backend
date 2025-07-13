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
        'titulo': handle_title_errors,
        'ruta': handle_route_errors,
        'medio': handle_media_errors,
        'fecha_inicio': handle_start_date_errors,
        'fecha_fin': handle_end_date_errors,
        'fechas': handle_fechas_errors,
        'origen': handle_origin_errors,
        'destino': handle_destination_errors,
        'km': handle_km_errors,
        'tiempo': handle_time_errors,
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
    
def handle_title_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_TITLE_REQUIRED:
        return {
            "message": MessagesES.ERROR_TITLE_REQUIRED,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif first_error == MessagesES.ERROR_TITLE_TYPE:
        return {
            "message": MessagesES.ERROR_TITLE_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }
    return {
        "message": MessagesES.ERROR_TITLE_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }


def handle_route_errors(errors):
    return {
        "message": MessagesES.ERROR_ROUTE_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }
    
def handle_media_errors(errors):
    return {
        "message": MessagesES.ERROR_MEDIA_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_start_date_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_DATE_START_PAST:
        return {
            "message": MessagesES.ERROR_DATE_START_PAST,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif first_error == MessagesES.ERROR_DATES:
        return {
            "message": MessagesES.ERROR_DATES,
            "status": status.HTTP_400_BAD_REQUEST
        }
    
    return {
        "message": MessagesES.ERROR_START_DATE_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_end_date_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_DATE_END_PAST:
        return {
            "message": MessagesES.ERROR_DATE_END_PAST,
            "status": status.HTTP_400_BAD_REQUEST
        }
    elif first_error == MessagesES.ERROR_DATES:
        return {
            "message": MessagesES.ERROR_DATES,
            "status": status.HTTP_400_BAD_REQUEST
        }
    
    return {
        "message": MessagesES.ERROR_END_DATE_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_fechas_errors(errors):
    return {
        "message": MessagesES.ERROR_DATES,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_origin_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_ORIGIN_TYPE:
        return {
            "message": MessagesES.ERROR_ORIGIN_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }
        
    return {
        "message": MessagesES.ERROR_ORIGIN_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }
    
def handle_destination_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_DESTINATION_TYPE:
        return {
            "message": MessagesES.ERROR_DESTINATION_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }
        
    return {
        "message": MessagesES.ERROR_DESTINATION_REQUIRED,
        "status": status.HTTP_400_BAD_REQUEST
    }

def handle_km_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_KM_TIME_TYPE:
        return {
            "message": MessagesES.ERROR_KM_TIME_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }

def handle_time_errors(errors):
    first_error = str(errors[0])
    
    if first_error == MessagesES.ERROR_KM_TIME_TYPE:
        return {
            "message": MessagesES.ERROR_KM_TIME_TYPE,
            "status": status.HTTP_400_BAD_REQUEST
        }

# Mapa de excepciones
EXCEPTION_HANDLERS = {
    AuthenticationFailed: handle_authentication_failed,
    ValidationError: handle_validation_error,
}
