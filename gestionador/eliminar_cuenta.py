#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

'''Eliminar cuenta en Fetchmail (usuario, correo, password-correo...)'''
def eliminar_cuenta_fetchmail(correo):
	subprocess.call(['bash','scripts/./eliminar_cuenta_fetchmail.sh', correo])

'''Eliminar correo en Postfix -> sasl_passwd'''
def eliminar_correo_postfix_sasl_passwd(correo):
	subprocess.call(['bash','scripts/./eliminar_correo_postfix_sasl_passwd.sh', correo])

'''Eliminar correo en Postfix -> relayhost_map'''
def eliminar_correo_postfix_relayhost_map(correo):
	subprocess.call(['bash','scripts/./eliminar_correo_postfix_relayhost_map.sh', correo])

'''Eliminar cuenta (correo local y correo externo) en Postfix -> Generic'''
def eliminar_cuenta_postfix_generic(usuario):
	subprocess.call(['bash','scripts/./eliminar_cuenta_postfix_generic.sh', usuario])

'''Eliminar correo Postfix -> Transport'''
def eliminar_correo_postfix_transport(correo):
	subprocess.call(['bash','scripts/./eliminar_correo_postfix_transport.sh', correo])

'''Eliminar correo local Postfix -> Transport'''
def eliminar_usuario_postfix_transport(usuario):
	subprocess.call(['bash','scripts/./eliminar_usuario_postfix_transport.sh', usuario])

'''Eliminamos cuentas en Fetchmail Postfix y Dovecot'''
def eliminar_correo(correo, usuario):
	eliminar_cuenta_fetchmail(correo)
	eliminar_correo_postfix_sasl_passwd(correo)
	eliminar_correo_postfix_relayhost_map(correo)
	eliminar_cuenta_postfix_generic(usuario)
	eliminar_correo_postfix_transport(correo)
	eliminar_usuario_postfix_transport(usuario)

'''Eliminamos usuario del sistema'''
def eliminar_usuario_unix(usuario):
	subprocess.call(['bash','scripts/./eliminar_usuario_unix.sh',usuario])
