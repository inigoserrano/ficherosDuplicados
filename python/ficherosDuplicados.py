import os
import hashlib

#
# Almaceno los ficheros que voy encontrando
#
ficheros = {}

#
# Parametros del programa
#
carpetTratar = []
filtrarTamano = False
filtrarMD5 = False
pedirBorrar = False


#
# Proceso la carpeta. Por cada fichero que encuentro lo busco dentro del diccionario
# ficheros. Si ya existe anado el directorio donde se encuentra, sino lo creo.
# 
def procesarCarpeta(tratarCarpeta):
    for laCarpeta, subFolders, files in os.walk(tratarCarpeta):
        for unFichero in files:
            if unFichero in ficheros:
                ficheros[unFichero][0] = ficheros[unFichero][0] + 1
                ficheros[unFichero][1].append(laCarpeta)
            else:
                ficheros[unFichero] = [1, [laCarpeta]]
#
# Devuelve si un fichero esta repetido, es decir existe un fichero con igual nombre en dos 
# o mas directorios
#
def estaRepetido(fichero):
    return ficheros[fichero][0] > 1

#
# Devuelve si todos los ficheros que tienen el mismo nombre tienen el mismo tamano
#
def mismoTamano(fichero):
    tamano = 0
    for unaCarpeta in ficheros[fichero][1]:
        if tamano == 0:
            tamano = os.path.getsize(unaCarpeta + "/" + fichero)
        if tamano != os.path.getsize(unaCarpeta + "/" + fichero):
            return False
    return True

#
# Calcula el md5 de un fichero
#
def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
            md5.update(chunk)
    return md5.hexdigest()

#
# Devuelve si todos ls ficheros que tienen el mismo nombre tienen el mismo md5 (hash)
#
def mismoMD5(fichero):
    tamano = 0
    for unaCarpeta in ficheros[fichero][1]:
        if tamano == 0:
            tamano = md5sum(unaCarpeta + "/" + fichero)
        if tamano != md5sum(unaCarpeta + "/" + fichero):
            return False
    return True


#
# Si se selecciona la opcion de borrar los ficheros. 
# Se muestran los ficheros junto con un numero identificativo y se pide al usuario que 
# seleccione el fichero a borrar. 0 Si no quiere borrar nada
#
def borrarDuplicado(unRepetido):
    print(" ")
    print("======================== Fichero: "+ unRepetido + " =======================")
    print(" Seleccione el numero del fichero a borrar: ")
    print(" ")
    print(" [0] No borrar ninguno ")
    rutas = []
    for unDirectorio in ficheros[unRepetido][1]:
        rutas.append(unDirectorio + "/" + unRepetido)
        print(" [" + str(len(rutas)) + "] " + unDirectorio + "/" + unRepetido) 
    print(" ")
    borrar = raw_input(" Cual Borrar ? ")
    if borrar != "0":
        print(" ")
        print(" Borrando: "+ rutas[int(borrar) - 1])
        os.remove(rutas[int(borrar) - 1])

#
# Si se selecciona la opcion de mostrar los ficheros duplicados
# Se muestran los ficheros
#
def informarDuplicado(unRepetido):
    print("======================== Fichero: "+ unRepetido + " =======================")             
    for unDirectorio in ficheros[unRepetido][1]:
        print(unDirectorio + "/" + unRepetido) 
    print(" ")


def ejecutar(pCarpetaTratar,pFiltrarTamano,pFiltrarMD5,pPedirBorrar):
    carpetaTratar=pCarpetaTratar
    filtrarTamano=pFiltrarTamano
    filtrarMD5=pFiltrarMD5
    pedirBorrar=pPedirBorrar
    
    for unaCarpeta in carpetaTratar:
        print(" Leyendo la carpeta: " + unaCarpeta)
        procesarCarpeta(unaCarpeta)

        print("    Buscando ficheros con identico nombre... ")
        repetidos = filter(estaRepetido, ficheros)  

    if filtrarTamano:
        print("    Descartando ficheros con diferente tamano... ")
        repetidos = filter(mismoTamano, repetidos)
    

    if filtrarMD5:
        print("    Descartando ficheros con diferente md5... ")
        repetidos = filter(mismoMD5, repetidos)

    print(" ")
    print(" Resumen: ")
    print("   Total Ficheros " + str(len(ficheros)))
    print("   Total Ficheros con identico nombre " + str(len(ficheros)))
    print("   Ficheros duplicados " + str(len(repetidos)))
    
    for unRepetido in repetidos:
        if pedirBorrar:
            borrarDuplicado(unRepetido)
        else:
            informarDuplicado(unRepetido)
    
