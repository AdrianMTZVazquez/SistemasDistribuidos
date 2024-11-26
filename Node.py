import threading
import socket
import time
import json
import ProcesadorTexto as PT

# Global Constants
DIRECCION_SERVERN = '127.0.0.1'
PUERTO_SERVERN    = 8001
THREAD_SEMPAHORE  = threading.Semaphore(3)
NOMBRE_ARCHIVO    = 'texto.txt'
TAG               = '[Node]'

# Global Variables
texto_leer = ''
seccion_leer = {}
servern_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
procesador_texto = PT.ProcesadorTexto(NOMBRE_ARCHIVO)

def ManejoConexion():
    global servern_socket
    
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break
        except TimeoutError:
            break
        except ConnectionResetError:
            break

def MandarMensajes():
    while True:
        try:
            print('Mandando mensajes...')
            THREAD_SEMPAHORE.acquire()
            try:
                servern_socket.send("Mandando mensajes".encode())
            finally:
                THREAD_SEMPAHORE.release()
            break
        except KeyboardInterrupt:
            break
        except TimeoutError:
            break
        except ConnectionResetError:
            break

def RecibirMensajes():
    while True:
        try:
            THREAD_SEMPAHORE.acquire()
            try:
                mensaje_sprocesar = servern_socket.recv(1024)
            finally:
                THREAD_SEMPAHORE.release()
            
            mensaje = json.loads(mensaje_sprocesar.decode())
            
            if 'Inicio' in mensaje.keys() or 'Fin' in mensaje.keys():
                print(f'{TAG} Iniciando la lectura...')
                seccion_texto = mensaje
                procesador_texto.LeerSeccionTexto(
                    seccion_texto['Inicio'],
                    seccion_texto['Fin']
                )
                
                resultado_frec = procesador_texto.ContarFrecPalabras()
                print(f'{TAG} Resultado: {resultado_frec}')
                
        except KeyboardInterrupt:
            break
        except TimeoutError:
            break
        except ConnectionResetError:
            break

def main():
    procesador_texto.LeerTexto()
    
    servern_socket.connect((DIRECCION_SERVERN, PUERTO_SERVERN))
    
    thread_manejo_conexion = threading.Thread(
        target = ManejoConexion,
        daemon = True
    )
    
    thread_mandar_mensajes = threading.Thread(
        target = MandarMensajes,
        daemon = True
    )
    
    thread_recibir_mensajes = threading.Thread(
        target = RecibirMensajes,
        daemon = True
    )
    
    thread_manejo_conexion.start()
    thread_mandar_mensajes.start()
    thread_recibir_mensajes.start()
    
    thread_manejo_conexion.join()
    thread_mandar_mensajes.join()
    thread_recibir_mensajes.join()

if __name__ == '__main__':    
    main()