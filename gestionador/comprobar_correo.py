#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo: comprobar_correo.py
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 15 de Diciembre de 2019
# Descripción: Módulo con funciones para comprobar si un correo está dado de alta en la base de datos o en algún
# archivo de configuración.
#
# Comprueba en /etc/fetchmailrc, /etc/postfix/sasl_passwd, /etc/postfix/relayhost_map, /etc/postfix/generic,
# y en /etc/postfix/transport .
import os
import re
import model

def comprobar_correo_bd (correo_bd ):

	correos_bd = model.get_cuentas_correos()

	for correo in correos_bd:

		if correo.correo == correo_bd:
			print "El Correo ya está dado de alta en la Base de Datos"
			return True;
	return False;


def comprobar_correo_existe( correo):

	comando = "/bin/bash scripts/./comprobar_correo_fetchmail.sh "+correo

	ejecucion = os.popen(comando)

	'''Quitamos el espacio final del resultado devuelto mediante expresion regular''' 
	resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 

	if resultado == "1":

		print "El correo ya está configurado en Fetchmail"

		return True

	if resultado == "0":
	
		comando = "/bin/bash scripts/./comprobar_correo_postfix_sasl_passwd.sh "+correo

		ejecucion = os.popen(comando)

		resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 

		if resultado == "1":

			print "El correo ya está configurado en Postfix"

			return True

		if resultado == "0":

			comando = "/bin/bash scripts/./comprobar_correo_postfix_relayhost_map.sh "+correo

			ejecucion = os.popen(comando)

			resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 

			if resultado == "1":

				print "El correo ya está configurado en Postfix"
		
				return True
		
			if resultado == "0":

				comando = "/bin/bash scripts/./comprobar_correo_postfix_generic.sh "+correo
	
				ejecucion = os.popen(comando)

				resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 

				if resultado == "1":

					print "El correo ya está configurado en Postfix"
		
					return True

				if resultado == "0":

					comando = "/bin/bash scripts/./comprobar_correo_postfix_transport.sh "+correo
		
					ejecucion = os.popen(comando)
	
					resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 
	
					if resultado == "1":
	
						print "El correo ya está configurado en Postfix"
		
						return True
			
					
					if resultado == "0":
						print "El correo no está configurado en el Sistema"
						return False

#comprobar_usuario_unix("amadews")
#comprobar_usuario_unix("bin")
#comprobar_usuario_unix("queso")
