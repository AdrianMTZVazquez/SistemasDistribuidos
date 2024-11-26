import MainServer as MS
import RPCServer as RS
import threading
import socket
import time
import json

# Global Constants
DIRECCION_SERVERN = '127.0.0.1'
PUERTO_SERVERN    = 8001
DIRECCION_MSERVER = '127.0.0.1'
PUERTO_MSERVER    = 8000
NUM_CONNECTIONS   = 10
THREAD_SEMAPHORE  = threading.Semaphore(10)
TAG               = '[ServerNode]'

# Global Variables
main_servidor = MS.MainServer(
    DIRECCION_SERVERN,
    PUERTO_SERVERN,
    NUM_CONNECTIONS,
    'ServerNode',
    DIRECCION_MSERVER,
    PUERTO_MSERVER)

rpc_functions = RS.RPCServer()

def ManejarConexion(addr):
    print('Conexión de', addr, 'aceptada')

def MandarMensajes(addr):
    while True:
        try:
            THREAD_SEMAPHORE.acquire()
            try:
                if main_servidor.usuarios[addr]['Seccion']['Asignado'] == 0:
                    print(f"{TAG} Enviando sección...")
                    main_servidor.usuarios[addr]['Socket'].send(
                        json.dumps(main_servidor.usuarios[addr]['Seccion']).encode()
                    )
            finally:
                THREAD_SEMAPHORE.release()
                main_servidor.usuarios[addr]['Seccion']['Asignado'] = 1
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except TimeoutError:
            break
        except ConnectionResetError:
            break
    
def RecibirMensajes(addr):
    while True:
        try:
            THREAD_SEMAPHORE.acquire()
            try:
                data = main_servidor.usuarios[addr]['Socket'].recv(1024)
            finally:
                THREAD_SEMAPHORE.release()
            print(data)
        except KeyboardInterrupt:
            break
        except TimeoutError:
            break
        except ConnectionResetError:
            break

def main():
    with open('texto.txt', 'r') as f:
        texto = f.read()
    
    secciones_texto = rpc_functions.SeparacionTexto(
        texto[:int(len(texto)/2)],
        NUM_CONNECTIONS
    )
    
    main_servidor.IniciarServidor()

    while True:
        client_socket, addr = main_servidor.AceptarConexion()

        for seccion in secciones_texto:
            if secciones_texto[seccion]['Asignado'] == False:
                secciones_texto[seccion]['Asignado'] = True
                THREAD_SEMAPHORE.acquire()
                try:
                    main_servidor.usuarios[addr[1]] = {
                        'Socket': client_socket,
                        'Seccion': {
                            'Inicio': secciones_texto[seccion]['Inicio'],
                            'Fin': secciones_texto[seccion]['Fin'],
                            'Asignado': 0
                        },
                    }
                finally:
                    THREAD_SEMAPHORE.release()
        
        thread_manejo_conexion = threading.Thread(
            target = ManejarConexion,
            args   = (addr[1],),
            daemon = True
        )
        
        thread_mandar_mensajes = threading.Thread(
            target = MandarMensajes,
            args   = (addr[1],),
            daemon = True
        )
        
        thread_recibir_mensajes = threading.Thread(
            target = RecibirMensajes,
            args   = (addr[1],),
            daemon = True
        )

        thread_manejo_conexion.start()
        thread_mandar_mensajes.start()
        thread_recibir_mensajes.start()

if __name__ == '__main__':
    main()
