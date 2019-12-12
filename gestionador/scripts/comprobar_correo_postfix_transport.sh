#!/bin/bash

transport_maps_file='/etc/postfix/transport'

if [[ $(awk '{print $1}' $transport_maps_file | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
else
        #echo "El correo NO existe."
	echo 0
fi
