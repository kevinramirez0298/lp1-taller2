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




        

