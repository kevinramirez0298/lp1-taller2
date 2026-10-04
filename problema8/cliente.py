#!/usr/bin/env python3

# ============================================================
# PROBLEMA 8 - CLIENTE
# TIC-TAC-TOE MULTIJUGADOR
# ============================================================

# 1. IMPORTAMOS LIBRERÍAS

import socket
import threading

# 2. CONFIGURACIÓN

HOST = "127.0.0.1"

PORT = 5002

# 3. VARIABLE PARA CONTROLAR EL CLIENTE

# Mientras sea True, el cliente seguirá funcionando.
activo = True
