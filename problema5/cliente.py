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

# 5. funcion enviar linea
def enviar_linea(conn, mensaje):

    # Enviar una línea de texto al servidor
    conn.sendall(mensaje + "\n".encode("utf-8"))  # Codificar el mensaje a bytes y enviarlo

# 6. funcion recibir linea
def recibir_linea(conn): 
    # recibe datos hasta encontrar un salto de linea
    datos = b""
    while b"\n" not in datos:
        parte = conn.recv(1)  # Recibir un byte a la vez
        if not parte:
            return None  # Si no hay más datos, devolver None
        datos += parte  # Agregar el byte recibido a los datos
    return datos.decode("utf-8").rstrip()  # Decodificar los datos a cadena y eliminar el salto de línea        


# 7. funcion conectar
def conectar():

   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket TCP
   conn.connect((HOST, PORT))  # Conectar al servidor
   return conn  # Devolver la conexión establecida


# 8. funcion LIST
def listar_archivos():

    conn = conectar()  # Establecer conexión con el servidor
    try: 
        enviar_linea(conn, "LIST")  # Enviar comando LIST al servidor
        respuesta = recibir_linea(conn)  # Recibir la respuesta del servidor
        if respuesta != "OK":
            print("Error al listar archivos:", respuesta)  # Mostrar mensaje de error si la respuesta no es OK
            return
        print("\nArchivos disponibles en el servidor:")  # Mostrar mensaje de archivos disponibles
        print("-------------------------------")

        cantidad = 0 

        while True:
            archivo = recibir_linea(conn)  # Recibir el nombre del archivo
            if archivo is None:
                break  # Salir del bucle si se recibe END

            if archivo == "END":
                break  # Salir del bucle si se recibe END   

            print("-", archivo)  # Mostrar el nombre del archivo
            cantidad += 1  # Incrementar la cantidad de archivos listados
        if cantidad == 0:
            print("No hay archivos disponibles en el servidor.")  # Mostrar mensaje si no hay archivos disponibles
    except Exception as e:
        print("Error al listar archivos:", str(e))  # Mostrar mensaje de error si ocurre una excepción
    finally:
        conn.close()  # Cerrar la conexión con el servidor

 # 9. funcion upload
def subir_archivo(ruta_archivo):
    if not os.path.isfile(ruta):
        print("El archivo no existe:", ruta_archivo)  # Mostrar mensaje si el archivo no existe
        return


    # 