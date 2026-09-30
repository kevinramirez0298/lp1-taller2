cat > servidor.py <<'PY'
#!/usr/bin/env python3

# PROBLEMA 5: TRANSFERENCIA DE ARCHIVOS

# 1. IMPORTAMOS LAS LIBRERÍAS
import socket # que permite la comunicación de red entre cliente y servidor TCP
import os # nos permite trabajar con carpetas y archibos y rurtas
import hashlib # nos permite generar un hash de un archivo para verificar que no fue alterado 


# 2. CONFIGURACIÓN DEL SERVIDOR

HOST = 'localhost'  # Dirección IP del servidor servira con nuestrocomputador.
PORT = 5001  # Puerto donde el servidor escucha las conexiones
CARPETA_ARCHIVOS = 'archivos'  # Carpeta donde se almacenarán los archivos recibidos
BUFFER_SIZE = 4096  # Tamaño del buffer para la transferencia de datos
