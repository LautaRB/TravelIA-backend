class MessagesES:
    # -Mensajes de error-

    #Error en los campos del superusuario
    ERROR_SUPERUSER_STAFF = "El superusuario debe tener is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "El superusuario debe tener is_superuser=True"
    
    #Error en los campos del usuario
    ERROR_USERNAME_REQUIRED = "El nombre de usuario es requerido."
    ERROR_USERNAME_TYPE = "El nombre de usuario no puede ser solo números."
    ERROR_USERNAME_SPACES = "El nombre de usuario no puede contener espacios."
    ERROR_PASSWORD_REQUIRED = "La contraseña es requerida."
    ERROR_EMAIL_REQUIRED = "El email es requerido."
    ERROR_REFRESH_REQUIRED = "El refresh token es requerido."
    ERROR_USER_ALREADY_EXISTS = "Ya existe un usuario con ese nombre."
    ERROR_EMAIL_ALREADY_EXISTS = "Ya existe un/a usuario con este/a email."
    
    #Error en la modificación del perfil del usuario
    ERROR_MODIFY_PROFILE = "No se pudo modificar el perfil del usuario."
    
    # Error en preferencias de usuario
    ERROR_CURRENCY_TYPE = "La moneda seleccionada no es válida."
    ERROR_DISTANCE_UNIT_TYPE = "La unidad de distancia seleccionada no es válida."
    
    #Error en la sesión
    ERROR_REGISTER = "No se pudo registrar el usuario."
    ERROR_LOGIN = "No se pudo iniciar sesión."
    ERROR_LOGOUT = "No se pudo cerrar sesión."
    ERROR_BAD_CREDENTIALS = "Credenciales inválidas. Intente nuevamente."
    
    #Error en los campos de la fecha
    ERROR_DATE_START_PAST = "La fecha de inicio no puede ser anterior a la fecha actual."
    ERROR_DATE_END_PAST = "La fecha de fin no puede ser anterior a la fecha actual."
    ERROR_DATES = "La fecha de inicio no puede ser posterior a la de fin."

    #Error en los campos de un viaje
    ERROR_TITLE_REQUIRED = "El título es requerido."
    ERROR_TITLE_TYPE = "El título no puede ser solo números."
    ERROR_START_DATE_REQUIRED = "La fecha de inicio es requerida."
    ERROR_END_DATE_REQUIRED = "La fecha de fin es requerida."
    
    #Error en la creación de un viaje
    ERROR_CREATE_TRIP = "No se pudo crear el viaje."
    
    #Error en la actualización de un viaje
    ERROR_UPDATE_TRIP = "No se pudo actualizar el viaje."
    
    #Error en la eliminación de un viaje
    ERROR_DELETE_TRIP = "No se pudo eliminar el viaje."
    
    #Error en los campos de la ruta
    ERROR_ROUTE_NAME_REQUIRED = "El nombre de la ruta es requerido."
    ERROR_ROUTE_NAME_TYPE = "El nombre de la ruta no puede ser solo números."
    ERROR_ORIGIN_REQUIRED = "El origen es requerido."
    ERROR_ORIGIN_TYPE = "El origen no puede ser solo números."
    ERROR_DESTINATION_REQUIRED = "El destino es requerido."
    ERROR_DESTINATION_TYPE = "El destino no puede ser solo números."
    ERROR_KM_TIME_TYPE = "Introduzca un número entero válido."
    
    #Error en la creación de una ruta
    ERROR_CREATE_ROUTE = "No se pudo crear la ruta."
    
    #Error ruta existente
    ERROR_ROUTE_EXISTS = "Ya existe esta ruta"
    
    #Error en la actualización de una ruta
    ERROR_UPDATE_ROUTE = "No se pudo actualizar la ruta."
    
    #Error en la eliminación de una ruta
    ERROR_DELETE_ROUTE = "No se pudo eliminar la ruta."
    
    #Error en los campos del medio
    ERROR_MEDIA_NAME_REQUIRED = "El nombre es requerido."
    ERROR_MEDIA_NAME_TYPE = "El nombre no puede ser solo números."
    ERROR_MEDIA_TYPE = "La opción ingresada no es una elección válida."
    ERROR_MEDIA_PRICE = "El precio debe ser un número decimal válido."
    
    #Error en la creación de un medio
    ERROR_CREATE_MEDIA = "No se pudo crear el medio."
    
    #Error medio existente
    ERROR_MEDIA_EXISTS = "Ya existe este medio"
    
    #Error en la actualización de un medio
    ERROR_UPDATE_MEDIA = "No se pudo actualizar el medio."
    
    #Error en la eliminación de un medio
    ERROR_DELETE_MEDIA = "No se pudo eliminar el medio."
    
    #Msj de valicacion generica
    GENERIC_VALIDATION_ERROR = "Datos inválidos"
    
    # -Mensajes de exito-
    
    #Exito en la sesión
    SUCCESS_LOGIN = "Login exitoso."
    SUCCESS_REGISTER = "Usuario registrado con éxito."
    SUCCESS_LOGOUT = "Sesión cerrada."
    
    #Exito en la modificación del perfil del usuario
    SUCCESS_MODIFY_PROFILE = "Perfil del usuario modificado con éxito."
    
    #exito en la creación de un viaje
    SUCCESS_CREATE_TRIP = "Viaje creado con éxito."
    
    #exito en la actualización de un viaje
    SUCCESS_UPDATE_TRIP = "Viaje actualizado con éxito."
    
    #exito en la eliminación de un viaje
    SUCCESS_DELETE_TRIP = "Viaje eliminado con éxito."
    
    #éxito en la creación de una ruta
    SUCCESS_CREATE_ROUTE = "Ruta creada con éxito."
    
    #exito en la actualización de una ruta
    SUCCESS_UPDATE_ROUTE = "Ruta actualizada con éxito."
    
    #exito en la eliminación de una ruta
    SUCCESS_DELETE_ROUTE = "Ruta eliminada con éxito."
    
    #exito en la creación de un medio
    SUCCESS_CREATE_MEDIA = "Medio creado con éxito."

    #exito en la actualización de un medio
    SUCCESS_UPDATE_MEDIA = "Medio actualizado con éxito."
    
    #exito en la eliminación de un medio
    SUCCESS_DELETE_MEDIA = "Medio eliminado con éxito."

class MessagesEN:
    # -Error messages-
    
    #Error in the superuser fields
    ERROR_SUPERUSER_STAFF = "Superuser must have is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "Superuser must have is_superuser=True"
    
    #Error in the user fields
    ERROR_USERNAME_REQUIRED = "Username is required."
    ERROR_USERNAME_TYPE = "Username cannot be only numbers."
    ERROR_USERNAME_SPACES = "Username cannot contain spaces."
    ERROR_PASSWORD_REQUIRED = "Password is required."
    ERROR_EMAIL_REQUIRED = "Email is required."
    ERROR_REFRESH_REQUIRED = "Refresh token is required."
    ERROR_USER_ALREADY_EXISTS = "A user with that username already exists."
    ERROR_EMAIL_ALREADY_EXISTS = "user with this email already exists."
    
    #Error in the modification of the user profile
    ERROR_MODIFY_PROFILE = "Could not modify user profile."
    
    # Error in user preferences
    ERROR_CURRENCY_TYPE = "The selected currency is not valid."
    ERROR_DISTANCE_UNIT_TYPE = "The selected distance unit is not valid."
    
    #Error in the session
    ERROR_REGISTER = "User registration failed."
    ERROR_LOGIN = "Login failed."
    ERROR_LOGOUT = "Logout failed."
    ERROR_BAD_CREDENTIALS = "Invalid credentials. Please try again."
   
    #Error in the date fields
    ERROR_DATE_START_PAST = "Start date cannot be in the past."
    RROR_DATE_END_PAST = "End date cannot be in the past."
    ERROR_DATES = "Start date cannot be after end date."

    #Error in the fields of a trip
    ERROR_TITLE_REQUIRED = "The title is required."
    ERROR_TITLE_TYPE = "The title cannot be only numbers."
    ERROR_START_DATE_REQUIRED = "The start date is required."
    ERROR_END_DATE_REQUIRED = "The end date is required."
    
    #Error in the creation of a trip
    ERROR_CREATE_TRIP = "Could not create the trip."
    
    #Error in the update of a trip
    ERROR_UPDATE_TRIP = "Could not update the trip."
    
    #Error in the deletion of a trip
    ERROR_DELETE_TRIP = "Could not delete the trip."
    
    #Error in the fields of a route
    ERROR_ROUTE_NAME_REQUIRED = "The name of the route is required."
    ERROR_ROUTE_NAME_TYPE = "The name of the route cannot be only numbers."
    ERROR_ORIGIN_REQUIRED = "The origin is required."
    ERROR_ORIGIN_TYPE = "The origin cannot be only numbers."
    ERROR_DESTINATION_REQUIRED = "The destination is required."
    ERROR_DESTINATION_TYPE = "The destination cannot be only numbers."
    ERROR_KM_TIME_TYPE = "Enter a valid integer."
    
    #Error in the creation of a route
    ERROR_CREATE_ROUTE = "Could not create the route."
    
    #Error route already exists
    ERROR_ROUTE_EXISTS = "Route already exists"
    
    #Error in the update of a route
    ERROR_UPDATE_ROUTE = "Could not update the route."
    
    #Error in the deletion of a route
    ERROR_DELETE_ROUTE = "Could not delete the route."
    
    #Error in the fields of a media
    ERROR_MEDIA_NAME_REQUIRED = "The name is required."
    ERROR_MEDIA_NAME_TYPE = "The name cannot be only numbers."
    ERROR_MEDIA_TYPE = "The selected option is not a valid choice."
    ERROR_MEDIA_PRICE = "The price must be a valid decimal number."
    
    #Error in the creation of a media
    ERROR_CREATE_MEDIA = "Could not create the media."
    
    #Error media already exists
    ERROR_MEDIA_EXISTS = "Media already exists"
    
    #Error in the update of a media
    ERROR_UPDATE_MEDIA = "Could not update the media."
    
    #Error in the deletion of a media
    ERROR_DELETE_MEDIA = "Could not delete the media."
    
    #Mssg of generic validation error
    GENERIC_VALIDATION_ERROR = "Invalid data"
    
    # -Success messages-
    
    #Success in the session
    SUCCESS_LOGIN = "Login successful."
    SUCCESS_REGISTER = "User registered successfully."
    SUCCESS_LOGOUT = "Logout successful."
    
    #Success in the modification of the user profile
    SUCCESS_MODIFY_PROFILE = "User profile modified successfully."
    
    #success in the creation of a trip
    SUCCESS_CREATE_TRIP = "Trip created successfully."
    
    #success in the update of a trip
    SUCCESS_UPDATE_TRIP = "Trip updated successfully."
    
    #success in the deletion of a trip
    SUCCESS_DELETE_TRIP = "Trip deleted successfully."
    
    #success in the creation of a route
    SUCCESS_CREATE_ROUTE = "Route created successfully."
    
    #success in the update of a route
    SUCCESS_UPDATE_ROUTE = "Route updated successfully."
    
    #success in the deletion of a route
    SUCCESS_DELETE_ROUTE = "Route deleted successfully."
    
    #success in the creation of a media
    SUCCESS_CREATE_MEDIA = "Media created successfully."
    
    #success in the update of a media
    SUCCESS_UPDATE_MEDIA = "Media updated successfully."
    
    #success in the deletion of a media
    SUCCESS_DELETE_MEDIA = "Media deleted successfully."
