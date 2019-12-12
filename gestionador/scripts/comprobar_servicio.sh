#!/bin/bash
if [[ $(/etc/init.d/$1 status | grep 'active (running)' | cut -d" " -f5-6 ) = "active (running)" ]]; then
        #echo "El servicio esta iniciado."
	echo 1
else
	#echo "El servicio no esta iniciado."
        echo 0
fi
