#1/usr/bin/env python3

# 1. IMPORTAMOS LAS LIBRERIAS.
import socket 
import os 
import hashlib

# 2. CONFIGURACION DEL CLIENTE
HOST = "localhost"  # IP del servidor
PORT = 5001         # Puerto del servidor
BUFFER_SIZE =  4096  # Tamaño del buffer para recibir datos
CARPETA_CLIENTE = "archivos_cliente"

# 3. funcion checksum_archivo
def checksum_archivo(ruta):

    sha256 = hashlib.sha256()  # Crear un objeto SHA-256
    with open(ruta, "rb") as archivo:
        while True:
            datos = archivo.read(BUFFER_SIZE)  # Leer el archivo en bloques
            if not datos:
                break
            sha256.update(datos)  # Actualizar el hash con los datos leídos
    return sha256.hexdigest()  # Devolver el hash en formato hexadecimal

# 4. funcion nombre_seguro
def nombre_seguro(nombre):
    # Reemplazar caracteres no permitidos en nombres de archivo
    nombre = os.path.basename(nombre)
    if nombre in ("", ".", ". ."):
        return None  # Devolver None si el nombre no es válido

# 5. funcion enviar linea
def enviar_linea(conn, mensaje):

    # Enviar una línea de texto al servidor
    conn.sendall((mensaje + "\n").encode("utf-8"))  # Codificar el mensaje a bytes y enviarlo

# 6. funcion recibir linea
def recibir_linea(conn): 
    # recibe datos hasta encontrar un salto de linea
    datos = b""
    while b"\n" not in datos:
        parte = conn.recv(1)  # Recibir un byte a la vez
        if not parte:
            return None  # Si no hay más datos, devolver None
        datos += parte  # Agregar el byte recibido a los datos
    return datos.decode("utf-8").rstrip()  # Decodificar los datos a cadena y eliminar el salto de línea        


# 7. funcion conectar
def conectar():

   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket TCP
   conn.connect((HOST, PORT))  # Conectar al servidor
   return conn  # Devolver la conexión establecida


# 8. funcion LIST
def listar_archivos():

    conn = conectar()  # Establecer conexión con el servidor
    try: 
        enviar_linea(conn, "LIST")  # Enviar comando LIST al servidor
        respuesta = recibir_linea(conn)  # Recibir la respuesta del servidor
        if respuesta != "OK":
            print("Error al listar archivos:", respuesta)  # Mostrar mensaje de error si la respuesta no es OK
            return
        print("\nArchivos disponibles en el servidor:")  # Mostrar mensaje de archivos disponibles
        print("-------------------------------")

        cantidad = 0 

        while True:
            archivo = recibir_linea(conn)  # Recibir el nombre del archivo
            if archivo is None:
                break  # Salir del bucle si se recibe END

            if archivo == "FIN":
                break  # Salir del bucle si se recibe END   

            print("-", archivo)  # Mostrar el nombre del archivo
            cantidad += 1  # Incrementar la cantidad de archivos listados
        if cantidad == 0:
            print("No hay archivos disponibles en el servidor.")  # Mostrar mensaje si no hay archivos disponibles
    except Exception as e:
        print("Error al listar archivos:", str(e))  # Mostrar mensaje de error si ocurre una excepción
    finally:
        conn.close()  # Cerrar la conexión con el servidor

 # 9. funcion upload
def subir_archivo(ruta):
    if not os.path.isfile(ruta):
        print("El archivo no existe:", ruta)  # Mostrar mensaje si el archivo no existe
        return

    # 9.1 Obtener nombre seguro
    nombre = nombre_seguro(
        os.path.basename(ruta)
    )

    if nombre is None:

        print("Nombre de archivo no válido.")

        return    

    # 10. calculamos el tamaño
    tamaño = os.path.getsize(ruta)  # Obtener el tamaño del archivo
    checksum_local = checksum_archivo(ruta)  # Calcular el checksum del archivo

    conn = conectar()  # Establecer conexión con el servidor
    try:
        enviar_linea(conn, f"UPLOAD {nombre}"
        )

        # 11. esperamos que el servidor esta listo
        respuesta = recibir_linea(conn)  # Recibir la respuesta del servidor
        if respuesta != "READY":
            print("Error al subir archivo:", respuesta)  # Mostrar mensaje de error si la respuesta no es READY
            return

        # 12. enviamos el tamaño y checksum
        enviar_linea(conn, str(tamaño)
        )

        print(f"\nSubiendo archivo: {nombre}") 
        print(f"Tamaño: {tamaño} bytes")

        # enviamos el arcihivo en bloques de 4096 bytes
        bytes_enviados = 0  # Inicializar contador de bytes enviados
        with open(ruta, "rb") as archivo:
            while bytes_enviados < tamaño:
                datos = archivo.read(BUFFER_SIZE)  # Leer el archivo en bloques
                if not datos:
                    break
                conn.sendall(datos)  # Enviar los datos al servidor
                bytes_enviados += len(datos)  # Incrementar el contador de bytes enviados
        print(f"bytes enviados: {bytes_enviados}/{tamaño}")  # Mostrar el progreso de bytes enviados

        # 13. recibimos checksum calculado por el servidor
        checksum_servidor = recibir_linea(conn)  # Recibir el checksum calculado

        print("Checksum local:", checksum_local)  # Mostrar el checksum local
        print("Checksum servidor:", checksum_servidor)  # Mostrar el checksum del servidor

        # comparamos ambos checkum
        if checksum_local == checksum_servidor:
            print("Archivo subido correctamente.")
        else:
            print("Error: Checksum no coincide. El archivo puede estar corrupto.")  # Mostrar mensaje de error si los checksums no coinciden
    except Exception as e:
        print("Error al subir archivo:", str(e))  # Mostrar mensaje de error si ocurre una excepción
    finally:
        conn.close()  # Cerrar la conexión con el servidor 

           
# 14. funcion download
def descargar_archivo(nombre):

    # validamos el nombre.
    nombre = nombre_seguro(nombre)  # Validar el nombre del archivo
    if nombre is None:
        print("Nombre de archivo no válido.")  # Mostrar mensaje si el nombre del archivo no es válido
        return

    # creamos la carpeta cliente si no existe
    os.makedirs(CARPETA_CLIENTE, exist_ok=True) 

    # ruta donde se guarda el archivo.
    ruta_destino = os.path.join
    (CARPETA_CLIENTE, nombre)  # Construir la ruta de destino del archivo

    conn = conectar()  # Establecer conexión con el servidor
    try:
        enviar_linea(
            conn, 
            f"DOWNLOAD {nombre}"
        )

        # 15. esperamos respuesta del servidor.
        respuesta = recibir_linea(conn)  # Recibir la respuesta del servidor
        if respuesta != "OK":
            print("Error al descargar archivo:", respuesta)  # Mostrar mensaje de error si la respuesta no es OK
            return
        tamaño_linea = recibir_linea(conn)  # Recibir la línea con el tamaño del archivo
        if tamaño_linea is None:
            print("Error al recibir el tamaño del archivo.")  # Mostrar mensaje de error si no se recibe el tamaño del archivo
            return
        tamaño = int(tamaño_linea)  # Convertir la línea recibida a entero
        # recibimos el checksum esperando.
        checksum_servidor = recibir_linea(conn)  # Recibir el checksum del servidor

        print(f"\nDescargando archivo: {nombre}")
        print(f"Tamaño: {tamaño} bytes")

        # 16. recibimos el archivo en bloques de 4096 bytes
        bytes_recibidos = 0  # Inicializar contador de bytes recibidos
        with open(ruta_destino, "wb") as archivo:
            while bytes_recibidos < tamaño:
                cantidad = min(
                    BUFFER_SIZE, 
                    tamaño - bytes_recibidos)  # Calcular la cantidad de bytes a recibir

                datos = conn.recv(cantidad)  # Recibir los datos del servidor
                if not datos:
                    break
                archivo.write(datos)  # Escribir los datos en el archivo
                bytes_recibidos += len(datos)  # Incrementar el contador de bytes recibidos
        print(f"bytes recibidos: {bytes_recibidos}")  # Mostrar

        # 17. calculamos el checksum del archivo descargado
        checksum_local = checksum_archivo(
            ruta_destino)  # Calcular el checksum del

        print("Checksum servidor:", checksum_servidor)  # Mostrar el checksum del servidor
        print("Checksum local:", checksum_local)  # Mostrar el checksum local

        # 18. verificamos entegridad.
        if checksum_local == checksum_servidor:
            print("Archivo descargado correctamente.")
        else:
            print("Error: Checksum no coincide. El archivo puede estar corrupto.")  # Mostrar mensaje de error si los checksums no coinciden

    except Exception as e:
        print("Error al descargar archivo:", str(e))  # Mostrar mensaje de error si ocurre una excepción
    finally:
        conn.close()  # Cerrar la conexión con el servidor


# 19. funcion mostrar menu
def mostrar_menu():
    print("\n--- Menú del Cliente ---")
    print("1. Listar archivos disponibles en el servidor")
    print("2. Subir archivo al servidor")
    print("3. Descargar archivo del servidor")
    print("4. Salir")
    print("------------------------")


# 20. funcion principal
def main():
    os.makedirs(
        CARPETA_CLIENTE, 
        exist_ok=True
    )  # 21. Crear la carpeta cliente si no existe    

    print("cliente de transferencia de archivos")
    print(f"servidor: {HOST}:{PORT}")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # 22. LIST
        if opcion == "1":
            listar_archivos()  # Llamar a la función para listar archivos

        # UPLOAD
        elif opcion == "2":
            ruta = input(
                "Ingrese la ruta del archivo a subir: ").strip()  # Solicitar la ruta del archivo al usuario
            subir_archivo(ruta)  # Llamar a la función para subir el archivo   

        # DOWNLOAD
        elif opcion == "3":
            nombre = input(
                "Ingrese el nombre del archivo a descargar: ").strip()  # Solicitar el nombre del archivo al usuario
            descargar_archivo(nombre)  # Llamar a la función para descargar el archivo


        # SALIR
        elif opcion == "4":
            print("Saliendo del cliente...")
            break  # Salir del bucle y finalizar el programa

        else:
            print("Opción no válida. Intente nuevamente.")  # Mostrar mensaje si la opción seleccionada no es válida

# 23. inicio del programa
if __name__ == "__main__":
    main()  # Llamar a la función principal para iniciar el programa      
