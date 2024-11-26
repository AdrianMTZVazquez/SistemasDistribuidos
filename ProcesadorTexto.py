
class ProcesadorTexto:
    def __init__(self,
                 _ntexto = "",
                 _num_secciones = 0):
        self.nombre_archivo = _ntexto
        self.num_secciones = _num_secciones
        self.texto_a_contar = ""
    
    def LeerTexto(self):
        with open(self.nombre_archivo,'r') as f:
            self.texto = f.read()
    
    def ContarFrecPalabras(self):
        frec_palabras = {}
        palabra = ""
        for letra in self.texto_a_contar:
            if letra.isalpha() and letra != " ":
                palabra += letra.lower()
            else:
                if palabra:
                    frec_palabras[palabra] = frec_palabras.get(palabra, 0) + 1
                    palabra = ""
        
        return frec_palabras

    def LeerSeccionTexto(self, inicio, fin):
        self.texto_a_contar = self.texto[inicio:fin]
    
    def SeparacionTexto(self):
        secciones_texto = {}
        
        for i in range(0,self.num_secciones):
            if i == 0:
                inicio = i * len(self.texto) // self.num_secciones
                fin    = (i+1) * len(self.texto) // self.num_secciones
            else:
                inicio = fin + 1
                fin    = (i + 1) * len(self.texto) // self.num_secciones
            
            if not self.texto[inicio].isalpha():
                inicio = self.ValidacionSeccion(inicio)
            
            if fin != len(self.texto):
                if self.texto[fin].isalpha():
                    fin = self.ValidacionSeccion(fin)
            
            secciones_texto[i] = {
                'Inicio': inicio,
                'Fin': fin,
                'Asignado': False
            }
        
        return secciones_texto
    
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