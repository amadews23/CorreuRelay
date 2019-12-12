#!/bin/bash

#smtp_generic_maps_file='/etc/postfix/generic'
smtp_generic_maps_file='generic'
if [[ $(awk '{print $2}' $smtp_generic_maps_file | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
else
        #echo "El correo NO existe."
	echo 0
fi
