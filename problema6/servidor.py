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

