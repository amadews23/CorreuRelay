#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo: crear_usuario.py
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 15 de Diciembre de 2019
# Descripción: Contiene una función para crear un usuario unix pásandole el nombre de usuario y password.
#

import os
import subprocess

def crear_usuario_unix(usuario, usuario_password):
	subprocess.call(['bash','scripts/./crear_usuario_unix.sh',usuario,usuario_password])

