class MessagesES:
    # Mensajes de error
    ERROR_SUPERUSER_STAFF = "El superusuario debe tener is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "El superusuario debe tener is_superuser=True"
    ERROR_USERNAME_REQUIRED = "El nombre de usuario es requerido."
    ERROR_USERNAME_TYPE = "El nombre de usuario no puede ser solo números."
    ERROR_PASSWORD_REQUIRED = "La contraseña es requerida."
    ERROR_EMAIL_REQUIRED = "El email es requerido."
    ERROR_REFRESH_REQUIRED = "El refresh token es requerido."
    ERROR_REGISTER = "No se pudo registrar el usuario."
    ERROR_LOGIN = "No se pudo iniciar sesión."
    ERROR_LOGOUT = "No se pudo cerrar sesión."
    ERROR_BAD_CREDENTIALS = "Credenciales inválidas. Intente nuevamente."
    ERROR_USER_ALREADY_EXISTS = "Ya existe un usuario con ese nombre."
    ERROR_EMAIL_ALREADY_EXISTS = "Ya existe un/a usuario con este/a email."
    ERROR_MODIFY_PROFILE = "No se pudo modificar el perfil del usuario."
    ERROR_DATE_PAST = "La fecha no puede ser anterior a la fecha actual."
    ERROR_DATES = "La fecha de inicio no puede ser posterior a la de fin."

    #Mensajes de exito
    SUCCESS_LOGIN = "Login exitoso."
    SUCCESS_REGISTER = "Usuario registrado con éxito."
    SUCCESS_LOGOUT = "Sesión cerrada."
    SUCCESS_MODIFY_PROFILE = "Perfil del usuario modificado con éxito."

class MessagesEN:
    #Error messages
    ERROR_SUPERUSER_STAFF = "Superuser must have is_staff=True"
    ERROR_SUPERUSER_SUPERUSER = "Superuser must have is_superuser=True"
    ERROR_USERNAME_REQUIRED = "Username is required."
    ERROR_USERNAME_TYPE = "Username cannot be only numbers."
    ERROR_PASSWORD_REQUIRED = "Password is required."
    ERROR_EMAIL_REQUIRED = "Email is required."
    ERROR_REFRESH_REQUIRED = "Refresh token is required."
    ERROR_REGISTER = "User registration failed."
    ERROR_LOGIN = "Login failed."
    ERROR_LOGOUT = "Logout failed."
    ERROR_BAD_CREDENTIALS = "Invalid credentials. Please try again."
    ERROR_USER_ALREADY_EXISTS = "A user with that username already exists."
    ERROR_EMAIL_ALREADY_EXISTS = "user with this email already exists."
    ERROR_MODIFY_PROFILE = "Could not modify user profile."
    ERROR_DATE_PAST = "Date cannot be in the past."
    ERROR_DATES = "Start date cannot be after end date."

    #Success messages
    SUCCESS_LOGIN = "Login successful."
    SUCCESS_REGISTER = "User registered successfully."
    SUCCESS_LOGOUT = "Logout successful."
    SUCCESS_MODIFY_PROFILE = "User profile modified successfully."

