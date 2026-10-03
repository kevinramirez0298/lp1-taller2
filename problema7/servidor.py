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


# 5. PROCESAR HTTPS - MÉTODO CONNECT
def manejar_connect(cliente, primera_linea):

    print("\n[HTTPS] Petición CONNECT recibida")

    print("[HTTPS]", primera_linea)

    partes = primera_linea.split()

    if len(partes) < 2:

        cliente.sendall(
            b"HTTP/1.1 400 Bad Request\r\n\r\n"
        )

        return

    destino = partes[1]
    # 5.1 Separamos HOST y PUERTO.
    
    if ":" in destino:

        host, puerto = destino.rsplit(":", 1)

        try:
            puerto = int(puerto)

        except ValueError:

            cliente.sendall(
                b"HTTP/1.1 400 Bad Request\r\n\r\n"
            )

            return

    else:

        host = destino
        puerto = 443

    print(f"[HTTPS] Destino: {host}:{puerto}")
    # 5.2 Nos conectamos al servidor HTTPS.
    try:

        servidor = socket.create_connection(
            (host, puerto),
            timeout=10
        )

    except Exception as error:

        print("[ERROR] No se pudo conectar:", error)

        cliente.sendall(
            b"HTTP/1.1 502 Bad Gateway\r\n\r\n"
        )

        return

    print("[HTTPS] Conexión establecida")

    respuesta = (
        "HTTP/1.1 200 Connection Established\r\n"
        "Proxy-Agent: Problema7-Proxy\r\n"
        "\r\n"
    )

    cliente.sendall(respuesta.encode())

    tunel_https(cliente, servidor)

