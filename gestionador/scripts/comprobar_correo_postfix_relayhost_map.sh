#!/bin/bash

sender_depend_relay_hostmaps_file='/etc/postfix/relay_hostmap'

if [[ $(awk '{print $1}' $sender_depend_relay_hostmaps_file | grep $1) = $1 ]]; then
        #echo "El correo ya existe."
	echo 1
else
        #echo "El correo NO existe."
	echo 0
fi
