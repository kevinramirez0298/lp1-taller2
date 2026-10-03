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

# 9. MOSTRAR LAS SALAS DISPONIBLES
def listar_salas():

    with lock:

        if not salas:

            return "No existen salas."

        texto = "Salas disponibles:\n"

        for nombre_sala in salas:

            cantidad = len(salas[nombre_sala])

            texto += f"- {nombre_sala} ({cantidad} usuarios)\n"

        return texto

# 10. MOSTRAR USUARIOS DE UNA SALA      
def listar_usuarios_sala(nombre_sala):

    with lock:

        # Verificamos si la sala existe.
        if nombre_sala not in salas:

            return f"La sala '{nombre_sala}' no existe."

        usuarios_lista = salas[nombre_sala]

        if not usuarios_lista:

            return f"La sala '{nombre_sala}' está vacía."

        texto = f"Usuarios en '{nombre_sala}':\n"

        for usuario in usuarios_lista:

            texto += f"- {usuario}\n"

        return texto

# 11. PROCESAR LOS COMANDOS DEL CLIENTE
def procesar_comando(nombre_usuario, socket_cliente, comando):

    # Eliminamos espacios al principio y al final.
    comando = comando.strip()

    # Si el cliente no escribió nada.
    if not comando:

        return True

    # 11.1 COMANDO LIST
    if comando.upper() == "LIST":

        enviar(
            socket_cliente,
            listar_salas()
        )

        return True

    # 11.2 COMANDO CREATE
    if comando.upper().startswith("CREATE "):

        partes = comando.split(maxsplit=1)

        nombre_sala = partes[1].strip()

        with lock:

            if nombre_sala in salas:

                enviar(
                    socket_cliente,
                    f"La sala '{nombre_sala}' ya existe."
                )

            else:

                # Creamos la sala.
                salas[nombre_sala] = set()

                # Guardamos en salas.json.
                guardar_salas()

                enviar(
                    socket_cliente,
                    f"Sala '{nombre_sala}' creada correctamente."
                )

        return True

    # 11.3 COMANDO JOIN
    if comando.upper().startswith("JOIN "):

        partes = comando.split(maxsplit=1)

        nombre_sala = partes[1].strip()

        with lock:

            # Verificamos si existe.
            if nombre_sala not in salas:

                enviar(
                    socket_cliente,
                    f"La sala '{nombre_sala}' no existe."
                )

                return True

            # Averiguamos si ya estaba en una sala.
            sala_anterior = usuarios_sala.get(nombre_usuario)

            # Si estaba en otra sala, lo sacamos.
            if sala_anterior is not None:

                salas[sala_anterior].discard(nombre_usuario)

            # Agregamos al usuario a la nueva sala.
            salas[nombre_sala].add(nombre_usuario)

            # Guardamos qué sala está utilizando.
            usuarios_sala[nombre_usuario] = nombre_sala

            guardar_salas()

        enviar(
            socket_cliente,
            f"Has entrado a la sala '{nombre_sala}'."
        )

        # Avisamos a los usuarios de la sala.
        enviar_a_sala(
            nombre_sala,
            f"[SISTEMA] {nombre_usuario} ha entrado a la sala."
        )

        return True


    # 11.4 COMANDO LEAVE
    if comando.upper() == "LEAVE":

        with lock:

            sala_actual = usuarios_sala.get(nombre_usuario)

            if sala_actual is None:

                enviar(
                    socket_cliente,
                    "No estás dentro de ninguna sala."
                )

                return True

            salas[sala_actual].discard(nombre_usuario)

            usuarios_sala.pop(nombre_usuario)

            guardar_salas()

        enviar(
            socket_cliente,
            f"Has salido de la sala '{sala_actual}'."
        )

        enviar_a_sala(
            sala_actual,
            f"[SISTEMA] {nombre_usuario} ha salido de la sala."
        )

        return True



    # 11.5 COMANDO USERS
    if comando.upper().startswith("USERS "):

        partes = comando.split(maxsplit=1)

        nombre_sala = partes[1].strip()

        enviar(
            socket_cliente,
            listar_usuarios_sala(nombre_sala)
        )

        return True

    # 11.6 COMANDO MSG
    if comando.upper().startswith("MSG "):

        partes = comando.split(maxsplit=2)

        # Necesitamos:
        #
        # MSG
        # sala
        # mensaje
        #
        if len(partes) < 3:

            enviar(
                socket_cliente,
                "Uso correcto: MSG sala mensaje"
            )

            return True

        nombre_sala = partes[1]

        mensaje = partes[2]

        with lock:

            sala_actual = usuarios_sala.get(nombre_usuario)

        # El usuario debe estar dentro de esa sala.
        if sala_actual != nombre_sala:

            enviar(
                socket_cliente,
                f"No estás dentro de la sala '{nombre_sala}'."
            )

            return True

        enviar_a_sala(
            nombre_sala,
            f"[{nombre_usuario}] {mensaje}"
        )

        return True
    

    # 11.7 COMANDO PRIVATE
    if comando.upper().startswith("PRIVATE "):

        partes = comando.split(maxsplit=2)

        
        if len(partes) < 3:

            enviar(
                socket_cliente,
                "Uso correcto: PRIVATE usuario mensaje"
            )

            return True

        destinatario = partes[1]

        mensaje = partes[2]

        with lock:

            if destinatario not in usuarios:

                enviar(
                    socket_cliente,
                    f"El usuario '{destinatario}' no está conectado."
                )

                return True

            socket_destinatario = usuarios[destinatario]

        # Enviamos solamente al destinatario.
        enviar(
            socket_destinatario,
            f"[PRIVADO de {nombre_usuario}] {mensaje}"
        )

        # Confirmamos al remitente.
        enviar(
            socket_cliente,
            f"[PRIVADO para {destinatario}] {mensaje}"
        )

        return True

    # 11.8 COMANDO HELP
    if comando.upper() == "HELP":

        ayuda = """
Comandos disponibles:

CREATE sala
    Crear una sala.

JOIN sala
    Entrar a una sala.

LEAVE
    Salir de la sala actual.

LIST
    Mostrar las salas disponibles.

USERS sala
    Mostrar usuarios de una sala.

MSG sala mensaje
    Enviar mensaje a una sala.

PRIVATE usuario mensaje
    Enviar mensaje privado.

HELP
    Mostrar esta ayuda.

QUIT
    Desconectarse.
"""

        enviar(
            socket_cliente,
            ayuda
        )

        return True

    # 11.9 COMANDO QUIT
    if comando.upper() == "QUIT":

        enviar(
            socket_cliente,
            "Desconectándote..."
        )

        return False



