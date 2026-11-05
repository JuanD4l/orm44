
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener la clave secreta
clave = os.getenv("FERNET_KEY")

if not clave:
    raise RuntimeError("No se encontró FERNET_KEY en el archivo .env")

# Crear el sistema de cifrado
cifrador = Fernet(clave.encode())


def cifrar_contrasena(contrasena):
    return cifrador.encrypt(contrasena.encode()).decode()


def descifrar_contrasena(contrasena_cifrada):
    return cifrador.decrypt(contrasena_cifrada.encode()).decode()
