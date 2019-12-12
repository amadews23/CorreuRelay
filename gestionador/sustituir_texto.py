#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo: sustituir_texto.py
# Autor: Bartolomé Vich Lozano
# Fecha: 29 de Octubre de 2019
# Descripción: Este programa sustituye linea de texto de un archivo origen en un archivo destino
# Se pasan como argumentos: el nombre del archivo origen y el destino
# 			    despues el texto a cambiar por el cual cambiar
# admite hasta dos patrones y dos textos que los sustituyen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Información adicional")
parser.add_argument("-s", "--source", help="Archivo origen")
parser.add_argument("-o", "--output", help="Archivo destino")
parser.add_argument("-p1", "--patron1", help="Patrón para sustituir")
parser.add_argument("-t1", "--texto1", help="Texto para insertar")
parser.add_argument("-p2", "--patron2", help="Patrón 2 para sustituir")
parser.add_argument("-t2", "--texto2", help="Texto 2 para insertar")
args = parser.parse_args()

def sustituir_texto(origen, destino, patron1, texto1, patron2="0", texto2="0", nlineas=1):

	for linea in origen:
		if linea.startswith(patron1):
			destino.write(texto1)

		elif linea.startswith(patron2) and nlineas != 1:
			destino.write(texto2)

		else:
			destino.write(linea)
	origen.close()
	destino.close()

try:
	origen = open(args.source,'r')
	destino = open(args.output, 'w')

except:
	print "Error: no se leyeron algunos de los archivos"

if args.source == None or args.output == None or args.patron1 == None or args.texto1 == None:
	print "La forma de usar el programa es:"
	print "python sustituir_texto.py -s Archivo origen -o Archivo destino -p1 patron_a_sustituir -t1 texto_para_a_escribir"
	print "O:"
	print "python sustituir_texto.py -s Archivo origen -o Archivo destino -p1 patron_a_sustituir -t1 texto_para_a_escribir-p2 	patron_a_sustituir -t2 texto_para_a_escribir"

elif args.patron2 != None and args.texto2 != None:

	sustituir_texto(origen, destino, args.patron1, args.texto1, args.patron2, args.texto2, 2)

else:
	sustituir_texto(origen, destino, args.patron1, args.texto1)
