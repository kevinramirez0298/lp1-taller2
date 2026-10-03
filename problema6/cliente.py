#!/usr/bin/env python3

# PROBLEMA 6 - CLIENTE DEL CHAT CON SALAS
# 1. IMPORTAR LIBRERÍAS
import socket
import threading


# 2. CONFIGURACIÓN
HOST = "localhost"

PORT = 5000

# 3. RECIBIR MENSAJES DEL SERVIDOR
def recibir_mensajes(socket_cliente):

    # Esta función se ejecuta en un hilo independiente.
    while True:

        try:

            # Esperamos información del servidor.
            datos = socket_cliente.recv(4096)

            # Si no llegan datos, el servidor cerró
            # la conexión.
            if not datos:

                print("\nServidor desconectado.")

                break

            # Convertimos los bytes a texto.
            mensaje = datos.decode("utf-8")

            print("\n" + mensaje)

            print("> ", end="", flush=True)


        except:

            print("\nConexión cerrada.")

            break
