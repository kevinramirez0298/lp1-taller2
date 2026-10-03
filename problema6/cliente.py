#!/usr/bin/env python3

# PROBLEMA 6 - CLIENTE DEL CHAT CON SALAS
# 1. IMPORTAR LIBRERÍAS
import socket
import threading


# 2. CONFIGURACIÓN
HOST = "localhost"

PORT = 5000

# 3. RECIBIR MENSAJES DEL SERVIDOR
def recibir_mensajes(socket_cliente):

    # Esta función se ejecuta en un hilo independiente.
    while True:

        try:

            # Esperamos información del servidor.
            datos = socket_cliente.recv(4096)

            # Si no llegan datos, el servidor cerró
            # la conexión.
            if not datos:

                print("\nServidor desconectado.")

                break

            # Convertimos los bytes a texto.
            mensaje = datos.decode("utf-8")

            print("\n" + mensaje)

            print("> ", end="", flush=True)


        except:

            print("\nConexión cerrada.")

            break


# 4. FUNCIÓN PRINCIPAL
def main():

    # 4.1. Creamos el socket del cliente.
    socket_cliente = socket.socket(
        socket.AF_INET, 
        socket.SOCK_STREAM
        )

    # 4.2. Conectamos con el servidor.
    try:

        socket_cliente.connect(
            (HOST, PORT)
            )
    except ConnectionRefusedError:

        print("No se pudo conectar con el servidor.")
        print("Asegúrate de que el servidor esté en ejecución.")
        return
    #4.3 . Creamos un hilo para recibir mensajes del servidor.
    hilo = threading.Thread(
        target=recibir_mensajes, 
        args=(socket_cliente,)
        )

    hilo.daemon = True 

    hilo.start()

    # 4.4 pedir nombre de usuario
    nombre = input()
    socket_cliente.sendall(
        (nombre + "\n").encode("utf-8")
        )

    # 4.5 mostrar menú de opciones
    print()
    print("=" * 50)
    print("CHAT CON SALAS")
    print("=" * 50)

    print("Escribe HELP para ver los comandos.")
    print()


    # 4.6 bucle del cliente
    while True:
        try:
            comando = input("> ")

            # Enviamos el comando al servidor.
            socket_cliente.sendall(
                (comando + "\n").encode("utf-8")
            )

            # Si escribimos QUIT, salimos.
            if comando.upper() == "QUIT":

                break


        except KeyboardInterrupt:

            print("\nSaliendo...")

            break


        except:

            print("Error de conexión.")

            break

    # 4.7 cerramos eñ socket
    socket_cliente.close()

# 5. INICIAR PROGRAMA
if __name__ == "__main__":
    main()

    
