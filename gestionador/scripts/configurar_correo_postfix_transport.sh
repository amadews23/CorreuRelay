#!/bin/bash

transport_maps_file='/etc/postfix/transport'

mi_host=$(cat /etc/hostname)
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $transport_maps_file $transport_maps_file${renombrado}

echo $1'@'$mi_host' local:' > $transport_maps_file
echo $2' local:' >> $transport_maps_file
cat $transport_maps_file${renombrado} >> $transport_maps_file

postmap ${transport_maps_file}
