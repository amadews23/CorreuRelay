#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Archivo: existe_texto.py
# Autor: Bartolomé Vich Lozano
# Fecha: 30 de Octubre de 2019
# Descripción: Este programa busca una linea de texto de un archivo
# Imprime 0 sino encuentra la linea, 1 si la encuentra
# Se pasan como argumentos: el nombre del archivo
# 			    la linea de texto a combrobar
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Información adicional")
parser.add_argument("-s", "--source", help="Archivo origen")
parser.add_argument("-p", "--patron", help="Patrón a encontrar")
args = parser.parse_args()

def existe_texto(origen, patron):

	encontrado=0
	for linea in origen:

		if linea.startswith(patron):

			encontrado=1
			break;


	origen.close()

	print encontrado

try:
	origen = open(args.source,'r')

except:

	print "Error: no se leyó el archivo"

if args.source == None or args.patron == None:

	print "La forma de usar el programa es:"
	print "python existe_texto.py -s Archivo origen -p patron_a_buscar"

else:
	existe_texto(origen, args.patron)

