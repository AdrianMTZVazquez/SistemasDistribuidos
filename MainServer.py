import socket

class MainServer:
    def __init__(self, 
                 _direccion, 
                 _puerto,
                 _numusers,
                 _tag,
                 _mserver_dir = None,
                 _mserver_puerto = None):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        
        self.direccion = _direccion
        self.puerto    = _puerto
        self.numusers  = _numusers
        self.TAG       = f"[{_tag}]"
        self.usuarios  = {}
        self.mserver   = _mserver_dir
        self.mpuerto   = _mserver_puerto
    
    def IniciarServidor(self):
        self.socket.bind((self.direccion, self.puerto))
        self.socket.listen(self.numusers)
        print(f"{self.TAG} Servidor iniciado en {self.direccion}:{self.puerto}...")
    
    def AceptarConexion(self):
        print(f"{self.TAG} Esperando conexion...")
        socket_cliente, addr = self.socket.accept()
        
        return (socket_cliente, addr)
        
    def ConectarMainServer(self):
        self.socket.connect((self.mserver, self.mpuerto))