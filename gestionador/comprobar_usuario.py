#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo: comprobar_usuario.py
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 15 de Diciembre de 2019
# Descripción: Módulo con funciones para comprobar si un usuario está dado de alta en la base de datos o en el Sistema.
#
# TODO PENDIENTE IMPLEMENTAR :comprobar -> /etc/fetchmailrc.
import os
import re
import model

def comprobar_usuario_bd (usuario_bd ):
	usuarios_bd = model.get_cuentas_usuarios()
	for usuario in usuarios_bd:

		if usuario.usuario == usuario_bd:
			print "El usuario ya está dado de alta en la Base de Datos"
			return True;
	return False;


def comprobar_usuario_unix( usuario_unix):

	comando = "/bin/bash scripts/./comprobar_usuario_unix.sh "+usuario_unix

	ejecucion = os.popen(comando)

	'''Quitamos el espacio final del resultado devuelto mediante expresion regular''' 
	resultado = re.sub(r"\s+$", "", ejecucion.read(), flags=re.UNICODE) 

	if resultado == "1":
		print "Es un usuario con Login"
		return True

	if resultado == "2":
		print "Es un usuario de Sistema"
		return True

	if resultado == "0":
		print "El usuario No Existe"
		return False

#comprobar_usuario_unix("amadews")
#comprobar_usuario_unix("bin")
#comprobar_usuario_unix("queso")
