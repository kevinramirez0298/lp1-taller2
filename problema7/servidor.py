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

# 6. PROCESAR PETICIÓN HTTP
def manejar_http(cliente, datos):

    # Convertimos los primeros datos a texto.

    try:

        texto = datos.decode(
            "iso-8859-1",
            errors="replace"
        )

    except Exception:

        cliente.close()
        return

    primera_linea = texto.split("\r\n")[0]

    print("\n[HTTP] Petición recibida:")
    print("[HTTP]", primera_linea)

    # Separamos la petición.
    
    partes = primera_linea.split()

    if len(partes) < 3:

        cliente.sendall(
            b"HTTP/1.1 400 Bad Request\r\n\r\n"
        )

        cliente.close()
        return

    metodo = partes[0]
    url = partes[1]
    version = partes[2]

    print("[HTTP] Método:", metodo)
    print("[HTTP] URL:", url)

    # Analizamos la URL.

    url_info = urlsplit(url)

    if url_info.hostname:

        host = url_info.hostname

        puerto = url_info.port

        if puerto is None:
            puerto = 80

        # La ruta que enviaremos al servidor.

        ruta = url_info.path

        if not ruta:
            ruta = "/"

        if url_info.query:

            ruta += "?" + url_info.query

    else:

        host = None

        puerto = 80

        for linea in texto.split("\r\n"):

            if linea.lower().startswith("host:"):

                host = linea.split(":", 1)[1].strip()

                break

        if host is None:

            cliente.sendall(
                b"HTTP/1.1 400 Bad Request\r\n\r\n"
            )

            cliente.close()
            return

        ruta = url

    if ":" in host:

        posible_host, posible_puerto = host.rsplit(":", 1)

        try:

            puerto = int(posible_puerto)
            host = posible_host

        except ValueError:

            pass

    print(f"[HTTP] Servidor destino: {host}:{puerto}")
    print(f"[HTTP] Ruta: {ruta}")

    # 7. CONECTAR CON EL SERVIDOR DESTINO
    try:

        servidor = socket.create_connection(
            (host, puerto),
            timeout=10
        )

    except Exception as error:

        print("[ERROR] No se pudo conectar al servidor:")
        print(error)

        respuesta = (
            "HTTP/1.1 502 Bad Gateway\r\n"
            "Content-Type: text/plain\r\n"              "Content-Length: 25\r\n"
            "\r\n"
            "Error servidor destino"
        )

        cliente.sendall(respuesta.encode())

        cliente.close()
        return

    print("[OK] Conectado al servidor destino")


    # 8. MODIFICAR LA PETICIÓN
    lineas = texto.split("\r\n")

    # Reemplazamos la primera línea.

    lineas[0] = f"{metodo} {ruta} {version}"

    # Buscamos el header Host y agregamos uno propio.

    tiene_proxy_header = False

    nuevas_lineas = []

    for linea in lineas:

        # Evitamos duplicar nuestro header.

        if linea.lower().startswith("proxy-agent:"):

            tiene_proxy_header = True

        nuevas_lineas.append(linea)

    # Agregamos un header para demostrar la modificación de headers.

    if not tiene_proxy_header:

        # Buscamos dónde termina la cabecera.

        try:

            posicion = nuevas_lineas.index("")

            nuevas_lineas.insert(
                posicion,
                "Proxy-Agent: Problema7-Proxy"
            )

        except ValueError:

            nuevas_lineas.append(
                "Proxy-Agent: Problema7-Proxy"
            )

    # Volvemos a construir la petición.

    nueva_peticion = "\r\n".join(nuevas_lineas)

    datos_modificados = nueva_peticion.encode(
        "iso-8859-1"
    )

    # 9. REENVIAR PETICIÓN AL SERVIDOR
    print("[HTTP] Reenviando petición...")

    try:

        enviar_todo(
            servidor,
            datos_modificados
        )

    except Exception as error:

        print("[ERROR] Error enviando datos:")
        print(error)

        servidor.close()
        cliente.close()

        return


    # 10. RECIBIR RESPUESTA DEL SERVIDOR
    print("[HTTP] Esperando respuesta...")

    try:

        while True:

            respuesta = servidor.recv(BUFFER_SIZE)

            # Si no hay más datos,
            # el servidor terminó la respuesta.

            if not respuesta:
                break

            # Mandamos la respuesta al cliente.

            cliente.sendall(respuesta)

    except Exception as error:

        print("[ERROR] Recibiendo respuesta:")
        print(error)

    # 11. CERRAR CONEXIONES
    servidor.close()
    cliente.close()

    print("[HTTP] Conexión terminada")

# 12. MANEJAR CADA CLIENTE
def manejar_cliente(cliente, direccion):
    """
    Atiende a un cliente conectado al proxy.
    """

    print("\n========================================")
    print("[NUEVO CLIENTE]", direccion)
    print("========================================")

    try:

        datos = cliente.recv(BUFFER_SIZE)

        if not datos:

            cliente.close()
            return

        texto = datos.decode(
            "iso-8859-1",
            errors="replace"
        )

        primera_linea = texto.split("\r\n")[0]

        print("[PETICIÓN]", primera_linea)


        if primera_linea.upper().startswith("CONNECT "):

            manejar_connect(
                cliente,
                primera_linea
            )

            return

        manejar_http(
            cliente,
            datos
        )

    except Exception as error:

        print("[ERROR] Cliente:", error)

        try:
            cliente.close()
        except:
            pass

# 13. FUNCIÓN PRINCIPAL
def main():

    # Creamos el socket TCP.

    servidor_proxy = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor_proxy.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor_proxy.bind(
        (HOST, PORT)
    )

    servidor_proxy.listen(10)

    print("========================================")
    print("       PROXY HTTP - PROBLEMA 7")
    print("========================================")
    print(f"Proxy escuchando en {HOST}:{PORT}")
    print("HTTP y HTTPS (CONNECT) habilitados")
    print("Presiona CTRL+C para detener")
    print("========================================")

    while True:

        cliente, direccion = servidor_proxy.accept()

        hilo = threading.Thread(
            target=manejar_cliente,
            args=(cliente, direccion),
            daemon=True
        )

        hilo.start()

