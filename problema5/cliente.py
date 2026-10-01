#1/usr/bin/env/ python3

# 1. IMPORTAMOS LAS LIBRERIAS.
import socket 
import os 
import hashlib

# 2. CONFIGURACION DEL CLIENTE
HOST = "localhost"  # IP del servidor
PORT = 5001         # Puerto del servidor
BUFFER_SIZE =  4096  # Tamaño del buffer para recibir datos


# 3. funcion checksum_archivo
def checksum_archivo(ruta):

    sha256 = hashlib.sha256()  # Crear un objeto SHA-256
    with open(ruta, "rb") as archivo:
        while True:
            datos = archivo.read(BUFFER_SIZE)  # Leer el archivo en bloques
            if not datos:
                break
            sha256.update(datos)  # Actualizar el hash con los datos leídos
    return sha256.hexdigest()  # Devolver el hash en formato hexadecimal

# 4. funcion nombre_seguro
def nombre_seguro(nombre):
    # Reemplazar caracteres no permitidos en nombres de archivo
    nombre = os.path.basename(nombre)
    if nombre in ("", ".", ". ."):
        return nombre