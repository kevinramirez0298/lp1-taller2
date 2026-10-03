#!/usr/bin/env python3

# PROBLEMA 6 - CHAT CON SALAS

# 1. IMPORTAR LIBRERÍAS
import socket
import threading
import json
import os


# 2. CONFIGURACIÓN DEL SERVIDOR
# Dirección donde escuchará el servidor.
HOST = "localhost"

# Puerto utilizado por el servidor.
PORT = 5000

# Archivo donde se guardan las salas.
ARCHIVO_SALAS = "salas.json"


# 3. VARIABLES COMPARTIDAS
usuarios = {} # Diccionario de usuarios conectados.
salas = {}
# Como varios hilos pueden modificar usuarios y salas al mismo tiempo, utilizamos un Lock.
lock = threading.Lock()

usuarios_sala = {} # Diccionario que indica en qué sala está cada usuario.

# 4. CARGAR LAS SALAS DESDE EL ARCHIVO
def cargar_salas():

    global salas

    # Si el archivo no existe, creamos una sala general.
    if not os.path.exists(ARCHIVO_SALAS):

        salas = {
            "general": set()
        }

        guardar_salas()
        return

    # Abrimos el archivo en modo lectura.
    with open(ARCHIVO_SALAS, "r", encoding="utf-8") as archivo:

        datos = json.load(archivo)

    # JSON no puede guardar conjuntos (set).
    # Por eso convertimos las listas nuevamente en sets.
    salas = {}

    for nombre_sala, usuarios_lista in datos.items():

        salas[nombre_sala] = set(usuarios_lista)


# 5. GUARDAR LAS SALAS EN EL ARCHIVO
def guardar_salas():
    datos = {}

    for nombre_sala, usuarios_set in salas.items():

        datos[nombre_sala] = list(usuarios_set)

    with open(ARCHIVO_SALAS, "w", encoding="utf-8") as archivo:
        json.dump(
            datos, 
            archivo, 
            indent=4, 
            ensure_ascii=False
            )

# 6. ENVIAR MENSAJE A UN CLIENTE
def enviar(socket_cliente, mensaje):

    try:

        socket_cliente.sendall(
            (mensaje + "\n").encode("utf-8")
        )

    except:

        # Si hay un error al enviar el mensaje, cerramos la conexión.
        pass

# 7. ENVIAR MENSAJE A TODOS LOS USUARIOS DE UNA SALA
def enviar_a_sala(nombre_sala, mensaje):

    # Lock porque estamos leyendo información compartida.
    with lock:

        # Verificamos que la sala exista.
        if nombre_sala not in salas:
            return

        # Hacemos una copia de los nombres.
        nombres_usuarios = list(salas[nombre_sala])

        # Obtenemos los sockets correspondientes.
        sockets = []

        for nombre_usuario in nombres_usuarios:

            if nombre_usuario in usuarios:

                sockets.append(
                    usuarios[nombre_usuario]
                )

    # Enviamos el mensaje.
    for socket_cliente in sockets:

        enviar(socket_cliente, mensaje)

# 8. ELIMINAR USUARIO DE SU SALA
def quitar_de_sala(nombre_usuario):

    with lock:

        # Averiguamos en qué sala estaba.
        sala_actual = usuarios_sala.get(nombre_usuario)

        # Si no estaba en ninguna sala, no hacemos nada.
        if sala_actual is None:
            return

        # Si la sala existe, eliminamos al usuario.
        if sala_actual in salas:

            salas[sala_actual].discard(nombre_usuario)

        # Eliminamos el registro del usuario.
        usuarios_sala.pop(nombre_usuario, None)

        # Guardamos el cambio.
        guardar_salas()

        

