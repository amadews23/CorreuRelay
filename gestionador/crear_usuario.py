#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

def crear_usuario_unix(usuario, usuario_password):
	subprocess.call(['bash','scripts/./crear_usuario_unix.sh',usuario,usuario_password])

