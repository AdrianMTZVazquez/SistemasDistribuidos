import threading
import MainServer as MS
import RPCServer as RS
import time

# Variables Globales
DIRECCION_MSERVER = '127.0.0.1'
PUERTO_MSERVER    = 5000
PUERTO_RPCSERVER  = 6000
SERVER_NODES      = 2
THREAD_LOCK       = threading.Lock()
NOMBRE_ARCHIVO    = 'texto.txt'

# GLOBAL VARIABLES
TEXTO = ''
SECCIONES_CONTADAS = 0
main_servidor = MS.MainServer(
    DIRECCION_MSERVER,
    PUERTO_MSERVER,
    SERVER_NODES,
    'MainServer'
)

def AceptarConexiones():
    while True:
        try:
            socket_cliente, addr = main_servidor.AceptarConexion()
            
            with THREAD_LOCK:
                main_servidor.usuarios[addr] = {
                    'Socket': socket_cliente,
                    'Seccion': addr
                }
            
            thread_manejador_cliente = threading.Thread(
                target = main_servidor.ManejarConexion,
                daemon = True
            )
            
            thread_manejador_cliente.start()
        except KeyboardInterrupt:
            print('Terminando la aplicacion...')
            exit()

def main():
    with open(NOMBRE_ARCHIVO,'r') as f:
        TEXTO = f.read()

    rpc_servidor = RS.RPCServer(
        DIRECCION_MSERVER,
        PUERTO_RPCSERVER
    )

    thread_rpcservidor = threading.Thread(
        target=rpc_servidor.IniciarServidorRPC
    )
    thread_rpcservidor.start()

    secciones_texto = rpc_servidor.SeparacionTexto(
        TEXTO,
        SERVER_NODES
    )

    main_servidor.IniciarServidor()

    thread_conexiones = threading.Thread(
        target = AceptarConexiones,
        daemon = True
    )

    thread_conexiones.start()
    
    while SECCIONES_CONTADAS < SERVER_NODES:
        pass

if __name__ == '__main__':
    main()