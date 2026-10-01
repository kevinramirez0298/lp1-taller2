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
        

                    # 21. Recibimos los datos por TCP.
                    datos = conn.recv(cantidad)
                    if not datos:  # Si no hay más datos, salimos del bucle
                        break

                    archivo.write(datos)  # Escribimos los datos en el archivo
                    bytes_recibidos += len(datos)  # Actualizamos el contador de bytes recibidos


            # 22. Calculamos el checksum del archivo recibido                
            checksum = checksum_archivo(ruta)

            # Enviamos el checksum al cliente
            enviar_linea(conn, checksum)


        # 23. COMANDO DOWNLOAD
        elif accion == "DOWNLOAD":
            if len(partes) != 2:
                enviar_linea(conn, "ERROR: No se proporcionó el nombre del archivo"
                )
                return

            # 23.1 comprobamos el nombre del archivo recibido para evitar problemas de seguridad.
            nombre = nombre_seguro(partes[1])  # Obtenemos un nombre seguro para el archivo
            if nombre is None:
                enviar_linea(conn, "ERROR: Nombre de archivo inválido"
                )
                return

            # 23.2 construimos la ruta del archivo a enviar
            ruta = os.path.join(
                CARPETA_ARCHIVOS, nombre
            )

            # 23.3 verificamos que el archivo exista
            if not os.path.isfile(ruta):
                enviar_linea(conn, "ERROR: Archivo no encontrado"
                )
                return

            # 23.4 obtenemos el tamaño del archivo
            tamaño = os.path.getsize(ruta)

            # 23.5 calculamos su checksum.
            checksum = checksum_archivo(ruta)

            # 23.6  enviamos al cliente que estamos listos para enviar el archivo
            enviar_linea(conn, "OK")

            # 23.7  enviamos el tamaño del archivo al cliente
            enviar_linea(conn, str(tamaño))

            # 23.8  enviamos el checksum del archivo al cliente
            enviar_linea(conn, checksum)

            # 23.9  Abrimos el archivo en modo binario para leer los datos a enviar
            with open(ruta, 'rb') as archivo:
                while True:
                    datos = archivo.read(BUFFER_SIZE)  # Leemos un bloque de datos
                    if not datos:  # Si no hay más datos, salimos del bucle
                        break

                    conn.sendall(datos)  # Enviamos los datos al cliente    


        # 24. COMANDO DESCONOCIDO
        else:
            enviar_linea(conn, "ERROR: Comando desconocido"
            )

    # 25. CONTROL DE ERRORES
    except Exception as e:
        enviar_linea(conn, f"ERROR: {str(e)}"
        )

    # 26. CERRAMOS LA CONEXIÓN
    finally:
        conn.close()  # Cerramos la conexión con el cliente


    # 27. FUNCIÓN: principal -main-
    def main():
        # 27.1 Creamos la carpeta de archivos si no existe
        os.makedirs(
            CARPETA_ARCHIVOS, exist_ok=True)

        # 28 Creamos un socket 
        servidor = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)

        # 29. reutilizar el puerto
        servidor.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1)

        # 30. asociar servidor con HOST Y PORT.
        servidor.bind(
            (HOST, PORT))

        # 30.1 poner el servidor a escuchar
        servidor.listen(5)  # Escuchamos hasta 5 conexiones entrantes

        # 30.2 mensajes informativos
        print(
            f"Servidor escuchando en {HOST}:{PORT}")

        print(
            f"Carpeta de archivos: {CARPETA_ARCHIVOS}")

        
        # 31. esperar clientes.
        while True:
            conn, addr = servidor.accept()  # Aceptamos una conexión entrante
            print(
                f"Cliente conectado desde {addr}")  # Mostramos la dirección del cliente
            manejar_cliente(conn)  # Manejamos la conexión con el cliente
            
            
    # 32. inicio del programa
    if __name__ == "__main__":
        main()  # Llamamos a la función principal
    