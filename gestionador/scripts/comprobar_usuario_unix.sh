#!/bin/bash

if [[ $(passwd -S -a | cut -d" " -f1-2 | grep P | cut -d" " -f1 | grep $1 ) = $1 ]]; then
        #echo "Es un usuario con Login."
	echo 1
elif [[ $(passwd -S -a | cut -d" " -f1-2 | grep L | cut -d" " -f1 | grep $1 ) = $1 ]]; then
        #echo "Es un usuario de Sistema."
	echo 2
else
        echo 0
	#echo "El usuario no existe."
fi
