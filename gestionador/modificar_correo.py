#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

'''Cambiamos en Fetchmail el correo que va asociado al usuario'''
def modificar_correo_fetchmail(correo, correo0):
	subprocess.call(['bash','scripts/./modificar_correo_fetchmail.sh',correo,correo0])

'''Cambiamos en Postfix-> sasl_password ,el nombre de cuenta de correo'''
def modificar_correo_postfix_sasl_password(correo, correo0):
	subprocess.call(['bash','scripts/./modificar_correo_postfix_sasl_passwd.sh',correo,corre0])

'''Cambiamos en Postfix-> Relayhost_map'''
def modificar_correo_postfix_relayhost_map(correo, correo0):
	subprocess.call(['bash','scripts/./modificar_correo_postfix_relayhost_map.sh',correo, corre0])

'''Cambiamos en Postfix-> Transport ,el nombre de su cuenta de correo local'''
def modificar_correo_postfix_transport(correo, correo0):
	subprocess.call(['bash','scripts/./modificar_correo_postfix_transport.sh',correo,correo0])

'''Cambiamos en Postfix-> Generic ,el nombre de su cuenta de correo local que está asociada al correo'''
def modificar_correo_postfix_generic(usuario, correo):
	subprocess.call(['bash','scripts/./modificar_correo_postfix_generic.sh',usuario,correo])

def modificar_correo_sistema(correo, correo0, usuario):

	modificar_correo_fetchmail(correo, correo0)
	modificar_correo_postfix_sasl_password(correo, correo0)
	modificar_correo_postfix_relayhost_map(correo, correo0)
	modificar_usuario_postfix_transport(correo, correo0)
	modificar_usuario_postfix_generic(usuario, correo)

'''Cambiamos en Fetchmail el password del correo'''
def modificar_correo_password_fetchmail(correo, password):
	subprocess.call(['bash','scripts/./modificar_correo_password_fetchmail.sh',correo,password])

'''Cambiamos en Postfix-> sasl_password ,el password de la cuenta de correo'''
def modificar_correo_password_postfix_sasl_password(correo, password):
	subprocess.call(['bash','scripts/./modificar_correo_password_postfix_sasl_passwd.sh',correo,password])

def modificar_correo_password_sistema(correo, password):
	modificar_correo_password_fetchmail(correo, password)
	modificar_correo_password_postfix_sasl_password(correo, password)

