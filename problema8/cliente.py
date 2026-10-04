#!/usr/bin/env python3

# ============================================================
# PROBLEMA 8 - CLIENTE
# TIC-TAC-TOE MULTIJUGADOR
# ============================================================

# 1. IMPORTAMOS LIBRERÍAS

import socket
import threading

# 2. CONFIGURACIÓN

HOST = "127.0.0.1"

PORT = 5002

# 3. VARIABLE PARA CONTROLAR EL CLIENTE

# Mientras sea True, el cliente seguirá funcionando.
activo = True


# 4. FUNCIÓN PARA RECIBIR MENSAJES
def recibir_mensajes(cliente):
    """
    Esta función escucha permanentemente al servidor.

    Se ejecuta en un hilo separado para que podamos:

    - recibir mensajes
    - y al mismo tiempo escribir comandos
    """

    global activo


    while activo:

        try:

            # Esperamos un mensaje del servidor.
            datos = cliente.recv(4096)


            # Si no recibimos datos,
            # el servidor se desconectó.
            if not datos:

                print("\nServidor desconectado.")

                activo = False

                break


            # Convertimos bytes a texto.
            mensaje = datos.decode()


            # Mostramos el mensaje.
            print(mensaje)


        except:

            activo = False

            break

# 5. FUNCIÓN PRINCIPAL
def main():

    global activo

    # CREAR SOCKET
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )


    # CONECTAR AL SERVIDOR

    try:

        cliente.connect(
            (HOST, PORT)
        )

    except ConnectionRefusedError:

        print()
        print("ERROR: No se pudo conectar al servidor.")
        print("Comprueba que servidor.py esté ejecutándose.")
        return

    # MENSAJE DE CONEXIÓN

    print()
    print("========================================")
    print("        CLIENTE TIC-TAC-TOE")
    print("========================================")
    print()
    print("Conectado al servidor.")
    print()


    # CREAR HILO PARA RECIBIR MENSAJES

    hilo = threading.Thread(
        target=recibir_mensajes,
        args=(cliente,),
        daemon=True
    )


    # Iniciamos el hilo.
    hilo.start()


    # MENÚ INICIAL

    print("Selecciona una opción:")
    print()
    print("1 - JUGAR")
    print("2 - ESPECTADOR")
    print()

    # LEER OPCIÓN

    opcion = input("Opción: ")


    # Enviamos la opción al servidor.
    cliente.sendall(
        (opcion + "\n").encode()
    )


