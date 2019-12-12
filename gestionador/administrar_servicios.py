#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import re

def reiniciar_servicio_fetchmail():

	subprocess.call(['/etc/init.d/fetchmail', 'restart'])

def reiniciar_servicio_postfix():

	subprocess.call(['/etc/init.d/postfix', 'restart'])

def reiniciar_servicio_dovecot():

	subprocess.call(['/etc/init.d/dovecot', 'restart'])

def reiniciar_servicios_todos():

	reiniciar_servicio_fetchmail()
	reiniciar_servicio_postfix()
	reiniciar_servicio_dovecot()

def comprobar_servicio_fetchmail():

	comando = "/bin/bash scripts/./comprobar_servicio.sh fetchmail"

	ejecucion = os.popen(comando)

	'''Quitamos el espacio final del resultado devuelto mediante expresion regular''' 
	resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 	

	if resultado == "1":

		print "Fetchmail está en ejecución."
		return True

	else:
		print "ERROR: Fetchmail NO está en ejecución."	
		return False

def comprobar_servicio_postfix():

	comando = "/bin/bash scripts/./comprobar_servicio.sh postfix"

	ejecucion = os.popen(comando)

	'''Quitamos el espacio final del resultado devuelto mediante expresion regular''' 
	resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 	

	if resultado == "1":

		print "Postfix está en ejecución."
		return True

	else:
		print "ERROR: Postfix NO está en ejecución."	
		return False

def comprobar_servicio_dovecot():

	comando = "/bin/bash scripts/./comprobar_servicio.sh dovecot"

	ejecucion = os.popen(comando)

	'''Quitamos el espacio final del resultado devuelto mediante expresion regular''' 
	resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 	

	if resultado == "1":

		print "Dovecot está en ejecución."
		return True

	else:
		print "ERROR: Dovecot NO está en ejecución."	
		return False

def comprobar_servicios_todos():

	if (comprobar_servicio_fetchmail() == True) and (comprobar_servicio_postfix() == True ) and (comprobar_servicio_dovecot() == True ):
		return True
	else:
		return False


