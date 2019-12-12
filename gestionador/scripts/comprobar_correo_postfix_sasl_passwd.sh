#!/bin/bash

sasl_password_file='/etc/postfix/sasl/sasl_passwd'

if [[ $(awk '{print $1}' $sasl_password_file | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
elif [[ $(awk '{print $2}' $sasl_password_file | cut -d":" -f1 | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
else
        #echo "El correo NO existe."
	echo 0
fi
