cat > servidor.py <<'PY'
#!/usr/bin/env python3

# PROBLEMA 5: TRANSFERENCIA DE ARCHIVOS

# 1. IMPORTAMOS LAS LIBRERÍAS
import socket # que permite la comunicación de red entre cliente y servidor TCP
import os # nos permite trabajar con carpetas y archibos y rurtas
import hashlib # nos permite generar un hash de un archivo para verificar que no fue alterado 


# 2. CONFIGURACIÓN DEL SERVIDOR
HOST = 'localhost'  # Dirección IP del servidor servira con nuestrocomputador.
PORT = 5001  # Puerto donde el servidor escucha las conexiones
CARPETA_ARCHIVOS = 'archivos'  # Carpeta donde se almacenarán los archivos recibidos
BUFFER_SIZE = 4096  # Tamaño del buffer para la transferencia de datos


# 3. FUNCIÓN: checksum_archivo
def checksum_archivo(ruta):
    sha256 = hashlib.sha256()  # Creamos un objeto hash SHA-256
    with open(ruta, 'rb') as archivo:  # Abrimos el archivo en modo binario
        # 4. repetimos hasta llegar al final del archivo
        while True: 
            datos = archivo.read(BUFFER_SIZE)  # Leemos solo 4096 bytes.
            if not datos:  # Si no hay más datos, salimos del bucle
                break

            sha256.update(datos)  # Actualizamos el hash con los datos leídos
    # 5. Devolvemos el hash en formato hexadecimal
    return sha256.hexdigest()  

# 6. FUNCIÓN: nombre_seguro
def nombre_seguro(nombre):
    nombre = os.path.basename(nombre)  # Obtenemos solo el nombre del archivo, sin la ruta
    if nombre in ("",".", ".."):  # Verificamos si el nombre es vacío o inválido
    
        return None  # Retornamos None si el nombre es inválido

    return nombre  # Retornamos el nombre seguro del archivo


# 7. FUNCIÓN: enviar_linea
def enviar_linea(conn, mensaje):
    # Convertimos el mensaje de texto a bytes utilizando UTF-8.
    conn.sendall( 
        (mensaje + "\n").encode("utf-8")
    )

# 8. FUNCIÓN: recibir_linea
def recibir_linea(conn):
    datos = b"" 
    while b"\n" not in datos:  # Leemos hasta encontrar un salto de línea
        parte = conn.recv(1)  # Recibimos un byte a la vez
        if not parte:  # Si no hay más datos, salimos del bucle
            return None  # Retornamos None si no se recibió ningún dato
        datos += parte  # Agregamos el byte recibido a los datos
    return datos.decode("utf-8").strip()  # Devolvemos la línea recibida, eliminando espacios en blanco

# 9. FUNCIÓN: manejar_cliente
def manejar_cliente(conn):
    # try permite controlar posibles errores.
    try:
        comando = recibir_linea(conn)  # Primero recibimos el comando enviado por el cliente.

        if comando is None:
            return  # Si no se recibió ningún comando, salimos de la función

        partes = comando.split(" ", 1)  # Dividimos el comando en partes

        accion = partes[0].upper() # La primera parte es la acción (UPLOAD o DOWNLOAD)


        # 10. COMANDO LIST
        if accion == "LIST":
            archivos = os.listdir(CARPETA_ARCHIVOS)  # Listamos los archivos en la carpeta
            archivos = [
                archivo
                for archivo in archivos
                if os.path.isfile(
                    os.path.join(
                        CARPETA_ARCHIVOS,
                        archivo
                    )
                )
            ]

            # 11.avisamos al cliente que la operacion fue correcta.
            enviar_linea(conn, "OK")

            # enviamos la lista de archivos al cliente, uno por línea
            for archivo in archivos:
                enviar_linea(conn, archivo)

            # 12. "FIN" indica al cliente que ya no quedan archivos por recibir
            enviar_linea(
                conn,
                "FIN"
            )

        # 13. COMANDO LIST
        if accion == "LIST":
            archivos = os.listdir(CARPETA_ARCHIVOS)  # Listamos los archivos en la carpeta
            archivos = [
                archivo
                for archivo in archivos
                if os.path.isfile(
                    os.path.join(
                        CARPETA_ARCHIVOS,
                        archivo
                    )
                )
            ]

            # 14.avisamos al cliente que la operacion fue correcta.
            enviar_linea(conn, "OK")

            # enviamos la lista de archivos al cliente, uno por línea
            for archivo in archivos:
                enviar_linea(conn, archivo)

            # 15. "FIN" indica al cliente que ya no quedan archivos por recibir
            enviar_linea(
                conn,
                "FIN"
            )


        # 16. COMANDO UPLOAD 
        elif accion == "UPLOAD":
            if len(partes) != 2:
                enviar_linea(conn, "ERROR: No se proporcionó el nombre del archivo"
                )
                return
            # comprobamos el nombre del archivo recibido para evitar problemas de seguridad.
            nombre = nombre_seguro(partes[1])  # Obtenemos un nombre seguro para el archivo
            if nombre is None:
                enviar_linea(conn, "ERROR: Nombre de archivo inválido"
                )
                return

            # 17. Comprobamos que el nombre sea seguro
            nombre = nombre_seguro(partes[1])  # Obtenemos un nombre seguro para el archivo
            if nombre is None:
                enviar_linea(conn, "ERROR: Nombre de archivo inválido"
                )
                return


                # 18. Avisamos al cliente que estamos listos para recibir el archivo
            enviar_linea(conn, "OK")

            # el cliente nos envia ahora el tamaño del archivo en bytes.
            tamaño_linea = recibir_linea(conn)
            if tamaño_linea is None:
                return

            # 19. Convertimos el tamaño del archivo a un entero
            tamaño = int(tamaño_linea)

            # contruimos la ruta donde se guardaremos el archivo.
            ruta = os.path.join(
                CARPETA_ARCHIVOS, nombre
                )

                # iniciamos el contador de bytes recibidos.
            bytes_recibidos = 0

            # 20. Abrimos el archivo en modo binario para escribir los datos recibidos
            with open(ruta, 'wb') as archivo:
                while bytes_recibidos < tamaño:  # Mientras no hayamos recibido todos los bytes
                    cantidad = min(
                        BUFFER_SIZE, tamaño - bytes_recibidos)  # Calculamos cuántos bytes leer
        

            

