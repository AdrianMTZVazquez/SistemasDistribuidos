from xmlrpc.server import SimpleXMLRPCServer

class RPCServer:
    def __init__(self, _direccion=None, _puerto=None):
        self.direccion = _direccion
        self.puerto    = _puerto
        
        if self.direccion is not None and self.puerto is not None:
            self.server = SimpleXMLRPCServer(
                (self.direccion, self.puerto),
                allow_none=True
            )
        
            self.RegistrarFunciones()
    
    def RegistrarFunciones(self):
        self.server.register_function(self.ContarFrecPalabras)
        self.server.register_function(self.SeparacionTexto)
        self.server.register_function(self.ValidacionSeccion)
    
    def IniciarServidorRPC(self):
        print('Use Control-C to exit')
        self.server.serve_forever()
    
    def ContarFrecPalabras(self, texto):
        frec_palabras = {}
        palabra = ""
        for letra in texto:
            if letra.isalpha() and letra != " ":
                palabra += letra.lower()
            else:
                if palabra:
                    frec_palabras[palabra] = frec_palabras.get(palabra, 0) + 1
                    palabra = ""
        
        return frec_palabras
    
    def ValidacionSeccion(self, texto, actual):
        first_pointer  = actual
        second_pointer = actual
        
        while True:
            first_pointer -= 1
            second_pointer += 1
            
            if not texto[first_pointer].isalpha():
                return first_pointer
                break
            
            if not texto[second_pointer].isalpha():
                return second_pointer
                break

    def SeparacionTexto(self, texto, num_secciones):
        secciones_texto = {}
        
        for i in range(0,num_secciones):
            if i == 0:
                inicio = i * len(texto) // num_secciones
                fin    = (i+1) * len(texto) // num_secciones
            else:
                inicio = fin + 1
                fin    = (i + 1) * len(texto) // num_secciones
            
            if not texto[inicio].isalpha():
                inicio = self.ValidacionSeccion(texto, inicio)
            
            if fin != len(texto):
                if texto[fin].isalpha():
                    fin = self.ValidacionSeccion(texto, fin)
            
            secciones_texto[i] = {
                'Inicio': inicio,
                'Fin': fin,
                'Asignado': False
            }
        
        return secciones_texto