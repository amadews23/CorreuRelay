#!/bin/bash

smtp_generic_maps_file='/etc/postfix/generic'

mi_host=$(cat /etc/hostname)
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')

#Realizamos copia por si algo sale mal
cp $smtp_generic_maps_file $smtp_generic_maps_file${renombrado}

python sustituir_texto.py -s $smtp_generic_maps_file${renombrado} -o  $smtp_generic_maps_file -p1 "$1@$mi_host" -t1 "$1@$mi_host	$2${salto}"

cat $smtp_generic_maps_file | sed 's/^[[:space:]]*//' > $smtp_generic_maps_file"-tmp"
#Renombramos temporal
mv $smtp_generic_maps_file"-tmp" $smtp_generic_maps_file

postmap ${smtp_generic_maps_file}
