#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""

import http.client

# TODO: Definir la dirección y puerto del servidor HTTP

# 1. Definir la dirección y puerto del servidor HTTP
HOST = "localhost"
PUERTO = 8000

# TODO: Crear una conexión HTTP con el servidor
# HTTPConnection permite establecer conexiones HTTP con servidores

# 2. Crear una conexión HTTP con el servidor
conexion = http.client.HTTPConnection(HOST, PUERTO)

# TODO: Realizar una petición GET al path raíz ('/')
# request() envía la petición HTTP al servidor
# Primer parámetro: método HTTP (GET, POST, etc.)
# Segundo parámetro: path del recurso solicitado

# 3. Realizar una petición GET al path raíz ('/')
conexion.request("GET", "/")

# TODO: Obtener la respuesta del servidor
# getresponse() devuelve un objeto HTTPResponse con los datos de la respuesta

# 4. Obtener la respuesta del servidor
respuesta = conexion.getresponse()

# TODO: Leer el contenido de la respuesta
# read() devuelve el cuerpo de la respuesta en bytes

# 5. Leer el contenido de la respuesta
contenido = respuesta.read()

# TODO: Decodificar los datos de bytes a string e imprimirlos
# decode() convierte los bytes a string usando UTF-8 por defecto

# 6. Decodificar los datos de bytes a string e imprimirlos
print(contenido.decode("utf-8"))

# TODO: Cerrar la conexión con el servidor

# 7. Cerrar la conexión con el servidor
conexion.close()