#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

'''Cambiamos el nombre de usuario, su directorio home y grupo'''
def modificar_usuario_unix(usuario, usuario0):
	subprocess.call(['bash','scripts/./modificar_usuario_unix.sh',usuario,usuario0])

'''Cambiamos en Fetchmail nombre del usuario al cual va su correo asociado'''
def modificar_usuario_fetchmail(usuario, usuario0):
	subprocess.call(['bash','scripts/./modificar_usuario_fetchmail.sh',usuario,usuario0])

'''Cambiamos en Postfix-> Transport ,el nombre de su cuenta de correo local'''
def modificar_usuario_postfix_transport(usuario, usuario0):
	subprocess.call(['bash','scripts/./modificar_usuario_postfix_transport.sh',usuario,usuario0])

'''Cambiamos en Postfix-> Generic ,el nombre de su cuenta de correo local que está asociada al correo'''
def modificar_usuario_postfix_generic(usuario, usuario0, correo):
	subprocess.call(['bash','scripts/./modificar_usuario_postfix_generic.sh',usuario,usuario0,correo])

def modificar_usuario_sistema(usuario, usuario0, correo):
	modificar_usuario_unix(usuario, usuario0)
	modificar_usuario_fetchmail(usuario, usuario0)
	modificar_usuario_postfix_transport(usuario, usuario0)
	modificar_usuario_postfix_generic(usuario, usuario0, correo)

def modificar_usuario_password(usuario, password):
	subprocess.call(['bash','scripts/./modificar_usuario_unix_password.sh',usuario,password])
#modificar_usuario_sistema("aurix", "auri")
