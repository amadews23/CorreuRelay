#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
