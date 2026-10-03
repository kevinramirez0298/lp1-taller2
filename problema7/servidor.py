#!/usr/bin/env python3

# PROBLEMA 7 - PROXY HTTP


# 1. IMPORTAMOS LAS LIBRERÍAS
import socket
import threading
from urllib.parse import urlsplit

# 2. CONFIGURACIÓN DEL PROXY
# Dirección donde escuchará el proxy.
HOST = "127.0.0.1"

# 2.1 Puerto donde escuchará el proxy.
PORT = 8080

# 2.2 Tamaño máximo de datos que recibimos de una vez.
BUFFER_SIZE = 4096

# 3. FUNCIÓN PARA ENVIAR DATOS COMPLETOS
def enviar_todo(sock, datos):
        
    # 3.1 sendall() intenta enviar todos los datos.
    sock.sendall(datos)

# 4. FUNCIÓN PARA CREAR UN TÚNEL HTTPS

def tunel_https(cliente, servidor):
    
    # 4.1 Ponemos los sockets en una lista.

    sockets = [cliente, servidor]

    try:

        while True:

            import select

            disponibles, _, errores = select.select(
                sockets,
                [],
                sockets,
                10
            )

            # 4.2 Si aparece algún error, terminamos.

            if errores:
                break

            # 4.3 Si no llegó información durante 10 segundos,
            if not disponibles:
                continue

            # 4.4Revisamos cuál socket recibió información.

            for sock in disponibles:

                try:

                    datos = sock.recv(BUFFER_SIZE)

                except ConnectionError:
                    return

                # 4.5 Si no hay datos significa que
                if not datos:
                    return

                # Si los datos vienen del cliente,
                if sock is cliente:

                    servidor.sendall(datos)

                else:

                    cliente.sendall(datos)

    finally:

        # Cerramos ambos sockets.

        try:
            cliente.close()
        except:
            pass

        try:
            servidor.close()
        except:
            pass



