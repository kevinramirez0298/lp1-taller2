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


# 4. LOCK
# Como pueden existir varios clientes al mismo tiempo,
# usamos un Lock para evitar que dos clientes modifiquen
# el tablero exactamente al mismo tiempo

lock = threading.Lock()

# 5. FUNCIÓN PARA ENVIAR MENSAJES
def enviar(cliente, mensaje):
    """
    Envía un mensaje a un cliente.

    cliente:
        conexión socket del cliente

    mensaje:
        texto que queremos enviar
    """

    try:
        cliente.sendall((mensaje + "\n").encode())

    except:
        # Si el cliente se desconectó,
        # simplemente ignoramos el error.
        pass

# 6. FUNCIÓN PARA MOSTRAR EL TABLERO
def mostrar_tablero():
    """
    Convierte el tablero en un texto bonito
    para enviarlo a los clientes.
    """

    texto = "\n"

    texto += " " + tablero[0] + " | " + tablero[1] + " | " + tablero[2] + "\n"
    texto += "---+---+---\n"

    texto += " " + tablero[3] + " | " + tablero[4] + " | " + tablero[5] + "\n"
    texto += "---+---+---\n"

    texto += " " + tablero[6] + " | " + tablero[7] + " | " + tablero[8] + "\n"

    return texto

# 7. FUNCIÓN PARA ENVIAR EL TABLERO A TODOS
def enviar_tablero():
    """
    Envía el tablero actualizado a:
    
    - Jugador X
    - Jugador O
    - Todos los espectadores
    """

    mensaje = "\n========== TABLERO ==========\n"
    mensaje += mostrar_tablero()
    mensaje += "=============================\n"

    # Enviar al jugador X
    if jugador_x is not None:
        enviar(jugador_x, mensaje)

    # Enviar al jugador O
    if jugador_o is not None:
        enviar(jugador_o, mensaje)

    # Enviar a los espectadores
    for espectador in espectadores:
        enviar(espectador, mensaje)

# 8. FUNCIÓN PARA NOTIFICAR A TODOS
def notificar(mensaje):
    """
    Envía un mensaje a todos los participantes.
    """

    # Enviar a X
    if jugador_x is not None:
        enviar(jugador_x, mensaje)

    # Enviar a O
    if jugador_o is not None:
        enviar(jugador_o, mensaje)

    # Enviar a espectadores
    for espectador in espectadores:
        enviar(espectador, mensaje)

# 9. FUNCIÓN PARA COMPROBAR GANADOR
def comprobar_ganador():
    """
    Comprueba si X o O consiguió tres posiciones
    seguidas.
    """

    # Todas las combinaciones posibles para ganar.
    combinaciones = [

        # Filas
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),

        # Columnas
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),

        # Diagonales
        (0, 4, 8),
        (2, 4, 6)
    ]

    # Revisamos cada combinación.
    for a, b, c in combinaciones:

        # Comprobamos que no estén vacías
        # y que las tres posiciones tengan
        # el mismo jugador.
        if (
            tablero[a] != " "
            and tablero[a] == tablero[b]
            and tablero[b] == tablero[c]
        ):

            # Devolvemos X u O.
            return tablero[a]

    # Si nadie ganó todavía.
    return None

# 10. FUNCIÓN PARA COMPROBAR EMPATE
def comprobar_empate():
    """
    Si no quedan posiciones vacías,
    significa que hubo empate.
    """

    return " " not in tablero

# 11. FUNCIÓN PARA REALIZAR UN MOVIMIENTO
def realizar_movimiento(cliente, simbolo, posicion):
    """
    Intenta realizar un movimiento.

    cliente:
        jugador que intenta jugar

    simbolo:
        X u O

    posicion:
        posición del tablero
    """

    global turno
    global partida_activa

    # LOCK
    # Protegemos el tablero para que dos jugadores
    # no puedan modificarlo simultáneamente.
    #
    with lock:

        # ----------------------------------------------------
        # Comprobar si es el turno correcto
        # ----------------------------------------------------

        if turno != simbolo:

            enviar(
                cliente,
                "ERROR: No es tu turno."
            )

            return


        # ----------------------------------------------------
        # Comprobar posición
        # ----------------------------------------------------

        if posicion < 1 or posicion > 9:

            enviar(
                cliente,
                "ERROR: La posición debe estar entre 1 y 9."
            )

            return


        # Convertimos de posición humana
        # a índice de Python.
        #
        # El usuario escribe:
        #
        # 1
        #
        # Python utiliza:
        #
        # 0
        #
        indice = posicion - 1


        # ----------------------------------------------------
        # Comprobar si la casilla está ocupada
        # ----------------------------------------------------

        if tablero[indice] != " ":

            enviar(
                cliente,
                "ERROR: Esa casilla ya está ocupada."
            )

            return


        # ----------------------------------------------------
        # REALIZAR EL MOVIMIENTO
        # ----------------------------------------------------

        tablero[indice] = simbolo


        # Avisamos a todos.
        notificar(
            f"El jugador {simbolo} jugó en la posición {posicion}."
        )


        # Actualizamos el tablero.
        enviar_tablero()


        # ----------------------------------------------------
        # COMPROBAR GANADOR
        # ----------------------------------------------------

        ganador = comprobar_ganador()

        if ganador is not None:

            notificar(
                f"\n🎉 GANADOR: El jugador {ganador} ha ganado."
            )

            partida_activa = False

            return


        # ----------------------------------------------------
        # COMPROBAR EMPATE
        # ----------------------------------------------------

        if comprobar_empate():

            notificar(
                "\n🤝 EMPATE. No quedan posiciones libres."
            )

            partida_activa = False

            return


        # ----------------------------------------------------
        # CAMBIAR TURNO
        # ----------------------------------------------------
        
        if turno == "X":
            turno = "O"
        else:
            turno = "X"


        # Avisamos de quién es el turno.
        notificar(
            f"\nAhora es el turno de {turno}."
        )


        



