texto = ''

with open('texto.txt','r') as f:
    texto = f.read()
print(len(texto))

def ValidacionSeccion(texto, actual):
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

def SeparacionTexto(texto, num_secciones):
    secciones_texto = {}
    
    for i in range(0,num_secciones):
        if i == 0:
            inicio = i * len(texto) // num_secciones
            fin    = (i+1) * len(texto) // num_secciones
        else:
            inicio = fin + 1
            fin    = (i + 1) * len(texto) // num_secciones
        
        if not texto[inicio].isalpha():
            inicio = ValidacionSeccion(texto, inicio)
        
        if fin != len(texto):
            if texto[fin].isalpha():
                fin = ValidacionSeccion(texto, fin)
        
        secciones_texto[i] = {
            'texto': texto[inicio:fin],
            'inicio': inicio,
            'fin': fin
        }
    
    return secciones_texto

print(SeparacionTexto(texto, 4))