#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""
# libreria que permite la comunicacion entre servidor y cliente.
import socket

# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)


# 1. configuracion del servidor, direccion IP del servidor 
HOST = "127.0.0.1"

# se agrega puerto para identificar a que servidor o aplicaion va dirigido.
PORT = 5000

# 2. se crea el socket del cliente.
client_socket = socket.socket(
    socket.AF_INET,   # Familia especificada a IPv4
    socket.SOCK_STREAM # Permite que los datos lleguen completos y ordenados
)

# TODO: Conectar el socket al servidor en la dirección y puerto especificados

# 3. conectarse al servidor, 
client_socket.connect((HOTS, PORT)) # connect()
 se establese una conexion con el servidor.

 # mostrar mensaje de conexion al servidor exitosa.
 print("conectado al servidor")

# TODO: Enviar datos al servidor (convertidos a bytes)
# sendall() asegura que todos los datos sean enviados

# crear el mensaje que se envia al servidor
mensaje = "hola servidor, soy el cliente."

# 4. se envia el mensaje al servidor
client_socket.sendall(mensaje.encode()) #sendall()envia mensaje al servidor,encode()convierte el texto en bytes.

# se muestra el mensaje que enviamos.
print("mensaje enviado:",mensaje)


# TODO: Recibir datos del servidor (hasta 1024 bytes)

# 5. recibir respuesta del servidor
datos = client_socket.recv(1024) # espera respuesta del servidor

# TODO: Decodificar e imprimir los datos recibidos

# 6. se conviete la respuesta en texto.
respuesta = datos.decode() # decode() convierte esos bytes en texto.


# TODO: Cerrar la conexión con el servidor

