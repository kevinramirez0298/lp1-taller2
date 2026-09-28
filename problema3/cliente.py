#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Cliente
Objetivo: Crear un cliente de chat que se conecte a un servidor y permita enviar/recibir mensajes en tiempo real
"""

import socket
import threading

def receive_messages():
    """
    Función ejecutada en un hilo separado para recibir mensajes del servidor
    de forma continua sin bloquear el hilo principal.
    """
    while True:
        # TODO: Recibir mensajes del servidor (hasta 1024 bytes) y decodificarlos
        # 1. recibir mensajes del servidor
        try:
            data = client_socket.recv(1024)

            # 2. si no llegan datos, el servidor se desconecto
            if not data:
                break

            # 3. descodificar el mensaje
            message = data.decode()    
        
            # Imprimir el mensaje recibido
            print(message)

        except ConnectionResetError:
            print("conexion con el servidor cerrada.")
            break


# Solicitar nombre de usuario al cliente
client_name = input("Cuál es tu nombre? ")

# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

# 4. Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: Conectar el socket al servidor en la dirección y puerto especificados

# 5. Conectar el socket al servidor
client_socket.connect(("127.0.0.1", 5000))

# TODO: Enviar el nombre del cliente al servidor (codificado a bytes)

# 6. Enviar el nombre del cliente al servidor
client_socket.send(client_name.encode())

# Crear y iniciar un hilo para recibir mensajes del servidor
# target: función que se ejecutará en el hilo
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Bucle principal en el hilo principal para enviar mensajes al servidor
while True:
    # Solicitar mensaje al usuario por consola
    message = input("Mensaje: ")
    # TODO: Codificar el mensaje a bytes y enviarlo al servidor

    # Codificar el mensaje a bytes y enviarlo
    client_socket.send(message.encode())
