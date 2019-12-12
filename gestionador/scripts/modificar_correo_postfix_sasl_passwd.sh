#!/bin/bash

#sasl_password_file='/etc/postfix/sasl/sasl_passwd'
sasl_password_file='sasl_passwd'
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')

#Realizamos copia por si algo sale mal
cp $sasl_password_file $sasl_password_file${renombrado}

password=$(cat $sasl_password_file${renombrado} | grep $2 | cut -d":" -f2)

python sustituir_texto.py -s $sasl_password_file${renombrado} -o  $sasl_password_file -p1 "$2	$2:" -t1 "$1	$1:${password} ${salto}"

#Quitamos el espacio que nos ha generado en la linea siguiente del cambio, copiamos a archivo temporal
cat $sasl_password_file | sed 's/^[[:space:]]*//' > $sasl_password_file"-tmp"
#Renombramos temporal
mv $sasl_password_file"-tmp" $sasl_password_file

#postmap ${sasl_password_file}
