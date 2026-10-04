#!/usr/bin/env python3

# ============================================================
# PROBLEMA 8 - SERVIDOR DE JUEGOS
# TIC-TAC-TOE MULTIJUGADOR
# ============================================================

# 1. IMPORTAMOS LAS LIBRERÍAS

import socket
import threading


# 2. CONFIGURACIÓN DEL SERVIDOR

# Dirección donde escuchará el servidor.
# 127.0.0.1 significa que trabajaremos en nuestra propia PC.
HOST = "127.0.0.1"

# Puerto que utilizaremos para este problema.
PORT = 5002


# 3. VARIABLES DEL JUEGO

# Tablero de 9 posiciones.
#
# Al principio todas las posiciones están vacías.
#
# Ejemplo:
#
#     1 | 2 | 3
#    ---+---+---
#     4 | 5 | 6
#    ---+---+---
#     7 | 8 | 9
#
tablero = [" "] * 9


# Jugadores de la partida.
# Aquí guardaremos:
# jugador X
# jugador O
jugador_x = None
jugador_o = None


# Lista de espectadores.
#
# Los espectadores pueden ver la partida,
# pero NO pueden realizar movimientos.
espectadores = []


# Variable que indica de quién es el turno.
# Puede ser:
# "X"
# "O"
turno = "X"


# Esta variable indica si la partida está activa.
partida_activa = False
