#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""
# se importa la libreria socket.
import socket

# TODO: Definir la dirección y puerto del servidor

# 1. configuracion del servidor
HOST = "127.0.0.1"  # Se conoce como localhost

# se agrega el puerto de conexion
PORT = 5000

# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

# 2. se crea el socket.
server_socket = socket.socket(
    socket.AF_INET, # Indica que utilizaremos IPv4.
    socket.SOCK_STREAM # Indica que utilizaremos TCP.
)

# TODO: Enlazar el socket a la dirección y puerto especificados

# 3. asociar el servidor con la direccion y el puerto
server_socket.bind((HOST, PORT)) # bind() conecta el socket del servidor con: HOST Y POST.


# TODO: Poner el socket en modo escucha
# El parámetro define el número máximo de conexiones en cola

# 4.poner al servidor a escuchar
server_socket.listen(1) # listen()hace que el servidor quede esperando la conexion de los clientes.

# mostrar mensaje si esta funcionando.
print("Servidor a la espera de conexiones ...")

# TODO: Aceptar una conexión entrante
# accept() bloquea hasta que llega una conexión
# conn: nuevo socket para comunicarse con el cliente
# addr: dirección y puerto del cliente

# 5. aceptar la conexion del cliente.
conn, addr = server_socket.accept() # Es el nuevo socket que utilizaremos para comunicarnos con ese cliente.

# se muestra quien se conecto
print(f"Conexión realizada por {addr}")

# TODO: Recibir datos del cliente (hasta 1024 bytes)
 
 # 6. recibir el mensaje del cliente
 datos = conn.recv(1024)

 # decode() convierte los bytes nuevamente en texto.
 mensaje = datos.decode()

 # mostramos el mensaje recibido
 print("mensaje recibido:", mensaje)
 
# TODO: Enviar respuesta al cliente (convertida a bytes)
# sendall() asegura que todos los datos sean enviados

# 7.preparar una respuesta
respuesta = "hola cliente, mensaje recibido correctamente"

# TODO: Cerrar la conexión con el cliente

