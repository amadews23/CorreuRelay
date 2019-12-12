#!/bin/bash
fetchmailrc_file='/etc/fetchmailrc'

if [[ $(awk '{print $2}' $fetchmailrc_file | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
else
        #echo "El correo NO existe."
	echo 0
fi
