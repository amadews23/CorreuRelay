#!/bin/bash
pedir_password() {
        read -s password_1
        echo "repita la contrasenya"
        read -s password_2
}
apt-get install sqlite3 -y
sqlite3 gestion.db 'CREATE TABLE "cuentas" ( `Id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `usuario` TEXT NOT NULL, `correo` TEXT NOT NULL )'
sqlite3 gestion.db 'CREATE TABLE "usuarios" ( `Id` INTEGER PRIMARY KEY AUTOINCREMENT, `usuario` TEXT NOT NULL UNIQUE, `password` TEXT NOT NULL )'
echo "Introduzca un nombre de usuario"
read usuario
echo "Introduzca la contrasenya"
	pedir_password
	while [ $password_1 != $password_2 ]; do
		echo "Haga el favor de poner bien la contrasenya para ${cuenta_por_defecto}"
		pedir_password
	done
sqlite3 gestion.db "INSERT INTO usuarios (usuario, password) VALUES('${usuario}','${password_1}');"
apt-get install python-pip -y
pip install web.py
