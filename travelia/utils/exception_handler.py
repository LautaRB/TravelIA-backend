from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Llamar al manejador por defecto de DRF para obtener la respuesta inicial
    response = exception_handler(exc, context)

    if response is not None:
            # Si DRF ya devolvió una respuesta, la personalizamos
            custom_response_data = {
                "error": True,
                "message": str(exc.__class__.__name__),
                "details": response.data
            }
            response.data = custom_response_data
    else:
        # Para errores no manejados por DRF
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