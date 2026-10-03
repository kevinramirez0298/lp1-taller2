#!/usr/bin/env python3

# PROBLEMA 7 - PRUEBA HTTPS
import socket
import ssl

# 1. CONFIGURACIÓN DEL PROXY
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080

# 2. SERVIDOR HTTPS QUE VAMOS A PROBAR
DESTINO_HOST = "example.com"
DESTINO_PORT = 443

# 3. FUNCIÓN PRINCIPAL
def main():

    print("========================================")
    print("       PRUEBA HTTPS - PROBLEMA 7")
    print("========================================")

    # Creamos un socket TCP.
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:

        # Nos conectamos al proxy.
        print(
            f"Conectando al proxy "
            f"{PROXY_HOST}:{PROXY_PORT}..."
        )

        cliente.connect(
            (PROXY_HOST, PROXY_PORT)
        )

        print("[OK] Conectado al proxy") 
        # Creamos la petición CONNECT.
        peticion_connect = (
            f"CONNECT {DESTINO_HOST}:{DESTINO_PORT} HTTP/1.1\r\n"
            f"Host: {DESTINO_HOST}:{DESTINO_PORT}\r\n"
            "\r\n"
        )

        print("\n========== CONNECT ==========")
        print(peticion_connect)


         # Enviamos CONNECT al proxy.
        cliente.sendall(
            peticion_connect.encode()
        )

        # Recibimos la respuesta del proxy.
        respuesta = cliente.recv(4096)

        print("========== RESPUESTA PROXY ==========")
        print(
            respuesta.decode(
                "iso-8859-1",
                errors="replace"
            )
        )


        # Comprobamos si el proxy creó el túnel.
        if b"200 Connection Established" not in respuesta:

            print("[ERROR] El proxy no creó el túnel.")

            cliente.close()

            return

        print("[OK] Túnel HTTPS creado")


