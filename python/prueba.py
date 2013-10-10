import argparse
import ficherosDuplicados

#
# Programa principal
#
parser = argparse.ArgumentParser(description='Localiza ficheros duplicados.')
parser.add_argument('directorio', metavar='directorio', type=str, nargs='+', help='directorio donde buscar')
parser.add_argument('--size', action='store_true', dest='filtrarTamano', help='comprobar tamano de los ficheros')
parser.add_argument('--md5', action='store_true', dest='filtrarMD5', help='comprobar hash md5 de los ficheros')
parser.add_argument('--rm', action='store_true', dest='pedirBorrar', help='pedir borrado de ficheros')

args = parser.parse_args()

ficherosDuplicados.ejecutar(args.directorio,args.filtrarTamano,args.filtrarMD5,args.pedirBorrar)