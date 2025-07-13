class MessagesES:
    # -Mensajes de error-

    #Error en los campos del superusuario
    ERROR_SUPERUSER_STAFF = "El superusuario debe tener is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "El superusuario debe tener is_superuser=True"
    
    #Error en los campos del usuario
    ERROR_USERNAME_REQUIRED = "El nombre de usuario es requerido."
    ERROR_USERNAME_TYPE = "El nombre de usuario no puede ser solo números."
    ERROR_PASSWORD_REQUIRED = "La contraseña es requerida."
    ERROR_EMAIL_REQUIRED = "El email es requerido."
    ERROR_REFRESH_REQUIRED = "El refresh token es requerido."
    ERROR_USER_ALREADY_EXISTS = "Ya existe un usuario con ese nombre."
    ERROR_EMAIL_ALREADY_EXISTS = "Ya existe un/a usuario con este/a email."
    
    #Error en la modificación del perfil del usuario
    ERROR_MODIFY_PROFILE = "No se pudo modificar el perfil del usuario."
    
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
    ERROR_ROUTE_REQUIRED = "La ruta es requerida."
    ERROR_MEDIA_REQUIRED = "El medio es requerido."
    ERROR_START_DATE_REQUIRED = "La fecha de inicio es requerida."
    ERROR_END_DATE_REQUIRED = "La fecha de fin es requerida."
    ERROR_CREATE_TRIP = "No se pudo crear el viaje."
    
    #Error en la actualización de un viaje
    ERROR_UPDATE_TRIP = "No se pudo actualizar el viaje."
    
    #Error en la eliminación de un viaje
    ERROR_DELETE_TRIP = "No se pudo eliminar el viaje."
    
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

class MessagesEN:
    # -Error messages-
    
    #Error in the superuser fields
    ERROR_SUPERUSER_STAFF = "Superuser must have is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "Superuser must have is_superuser=True"
    
    #Error in the user fields
    ERROR_USERNAME_REQUIRED = "Username is required."
    ERROR_USERNAME_TYPE = "Username cannot be only numbers."
    ERROR_PASSWORD_REQUIRED = "Password is required."
    ERROR_EMAIL_REQUIRED = "Email is required."
    ERROR_REFRESH_REQUIRED = "Refresh token is required."
    ERROR_USER_ALREADY_EXISTS = "A user with that username already exists."
    ERROR_EMAIL_ALREADY_EXISTS = "user with this email already exists."
    
    #Error in the modification of the user profile
    ERROR_MODIFY_PROFILE = "Could not modify user profile."
    
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
    ERROR_ROUTE_REQUIRED = "The route is required."
    ERROR_MEDIA_REQUIRED = "The media is required."
    ERROR_START_DATE_REQUIRED = "The start date is required."
    ERROR_END_DATE_REQUIRED = "The end date is required."
    ERROR_CREATE_TRIP = "Could not create the trip."
    
    #Error in the update of a trip
    ERROR_UPDATE_TRIP = "Could not update the trip."
    
    #Error in the deletion of a trip
    ERROR_DELETE_TRIP = "Could not delete the trip."
    
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
