from rest_framework.views import exception_handler
from .exceptions import EXCEPTION_HANDLERS
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        handler = EXCEPTION_HANDLERS.get(type(exc)) #obtener el tipo de excepcion

        if handler:
            result = handler(exc, response)
            message = result["message"]
            estado = result["status"]
        else: #default
            message = str(exc.__class__.__name__)
            estado = response.status_code

        response.data = {
            "error": True,
            "status": estado,
            "message": message,
        }

        return response

    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response(
        {
            "error": True,
            "message": "Error interno del servidor",
            "details": str(exc)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )