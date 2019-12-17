#!/bin/bash

transport_maps_file='/etc/postfix/transport'

mi_host=$(cat /etc/hostname)
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')

#Realizamos copia por si algo sale mal
cp $transport_maps_file $transport_maps_file${renombrado}

python sustituir_texto.py -s $transport_maps_file${renombrado} -o  $transport_maps_file -p1 "$2" -t1 "$1 local:${salto}"

cat $transport_maps_file | sed 's/^[[:space:]]*//' > $transport_maps_file"-tmp"
#Renombramos temporal
mv $transport_maps_file"-tmp" $transport_maps_file

postmap ${transport_maps_file}
