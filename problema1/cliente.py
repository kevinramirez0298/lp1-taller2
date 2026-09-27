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

# TODO: Enviar datos al servidor (convertidos a bytes)
# sendall() asegura que todos los datos sean enviados

# TODO: Recibir datos del servidor (hasta 1024 bytes)

# TODO: Decodificar e imprimir los datos recibidos

# TODO: Cerrar la conexión con el servidor

