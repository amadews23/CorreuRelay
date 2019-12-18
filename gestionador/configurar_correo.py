#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo: configurar_correo.py
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 15 de Diciembre de 2019
# Descripción: Módulo con funciones para configurar un correo en archivos de configuración.
#
# Configura una cuenta de correo en /etc/fetchmailrc, /etc/postfix/sasl_passwd, /etc/postfix/relayhost_map, /etc/postfix/generic,
# y en /etc/postfix/transport .
import os
import subprocess

'''Configurar Fetchmail'''
def configurar_correo_fetchmail(correo, correo_password, usuario):
	subprocess.call(['bash','scripts/./configurar_correo_fetchmail.sh', correo, correo_password, usuario])

'''Postfix -> sasl_passwd'''
def configurar_correo_postfix_sasl_passwd(correo, correo_password):
	subprocess.call(['bash','scripts/./configurar_correo_postfix_sasl_passwd.sh', correo, correo_password])

'''Postfix -> relayhost_map'''
def configurar_correo_postfix_relayhost_map(correo):

	subprocess.call(['bash','scripts/./configurar_correo_postfix_relayhost_map.sh', correo])

'''Postfix -> Generic'''
def configurar_correo_postfix_generic(usuario, correo):
	subprocess.call(['bash','scripts/./configurar_correo_postfix_generic.sh', usuario, correo])

'''Postfix -> Transport'''
def configurar_correo_postfix_transport(usuario, correo):
	subprocess.call(['bash','scripts/./configurar_correo_postfix_transport.sh', usuario, correo])


def configurar_correo(correo, correo_password, usuario):

	configurar_correo_fetchmail(correo, correo_password, usuario)
	configurar_correo_postfix_sasl_passwd(correo, correo_password)		
	configurar_correo_postfix_relayhost_map(correo)
	configurar_correo_postfix_generic(usuario, correo)
	configurar_correo_postfix_transport(usuario, correo)
