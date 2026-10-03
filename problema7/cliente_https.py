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


        # 4. CREAMOS SSL/TLS
        contexto = ssl.create_default_context()

        cliente_ssl = contexto.wrap_socket(
            cliente,
            server_hostname=DESTINO_HOST
        )

        print("[OK] Conexión TLS establecida")


        # 5. ENVIAMOS PETICIÓN HTTPS
        peticion_https = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {DESTINO_HOST}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        print("\n========== PETICIÓN HTTPS ==========")
        print(peticion_https)

        cliente_ssl.sendall(
            peticion_https.encode()
        )

        # 6. RECIBIMOS RESPUESTA HTTPS
        respuesta_completa = b""

        while True:

            datos = cliente_ssl.recv(4096)

            if not datos:
                break

            respuesta_completa += datos

        print("\n========== RESPUESTA HTTPS ==========")

        print(
            respuesta_completa.decode(
                "utf-8",
                errors="replace"
            )
        )

        print("\n========== FIN ==========")

        # Cerramos la conexión TLS.
        cliente_ssl.close()

        print("[OK] Conexión HTTPS cerrada")

    except Exception as error:

        print("\n[ERROR]")
        print(error)

        try:
            cliente.close()
        except:
            pass

# 7. INICIO DEL PROGRAMA
if __name__ == "__main__":

    main()
    