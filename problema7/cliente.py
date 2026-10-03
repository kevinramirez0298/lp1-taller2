#!/usr/bin/env python3

# PROBLEMA 7 - CLIENTE DE PRUEBA

# 1. IMPORTAMOS SOCKET
import socket

# 2. CONFIGURACIÓN DEL CLIENTE
# Dirección del proxy.
PROXY_HOST = "127.0.0.1"

# Puerto del proxy.

PROXY_PORT = 8080

# 3. FUNCIÓN PRINCIPAL
def main():
    print("========================================")
    print("       CLIENTE HTTP - PROBLEMA 7")
    print("========================================")

    # 3.1 Creamos el socket TCP.
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        # 3.2 Conectamos con el proxy.
        print(
            f"conectado al procy "
            f"{PROXY_HOST}:{PROXY_PORT}"
        )
        
        cliente.connect(
            (PROXY_HOST, PROXY_PORT)
        )
    
        print("[ok] conectado añ proxy")

        host = "example.com"

        # Construimos una petición HTTP.
        
        peticion = (
            f"GET http://{host}/ HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        # Mostramos lo que vamos a enviar.
        
        print("\n========== PETICIÓN ==========")
        print(peticion)

        # Enviamos la petición al PROXY.
        
        cliente.sendall(
            peticion.encode()
        )

        print("[OK] Petición enviada")

        # Recibimos la respuesta.
        
        respuesta_completa = b""

        while True:

            datos = cliente.recv(4096)

            if not datos:
                break

            respuesta_completa += datos

        # Convertimos la respuesta a texto.
        
        respuesta = respuesta_completa.decode(
            "iso-8859-1",
            errors="replace"
        )

        # Mostramos la respuesta.

        print("\n========== RESPUESTA ==========")

        print(respuesta)

        print("\n========== FIN ==========")

    except Exception as error:

        print("[ERROR]")
        print(error)

    finally:

        # ----------------------------------------------------
        # Cerramos el socket.
        # ----------------------------------------------------

        cliente.close()


