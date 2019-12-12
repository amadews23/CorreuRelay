#!/bin/bash

smtp_generic_maps_file='/etc/postfix/generic'

mi_host=$(cat /etc/hostname)
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $smtp_generic_maps_file $smtp_generic_maps_file${renombrado}

echo $1'@'$mi_host'	'$2 > $smtp_generic_maps_file
cat $smtp_generic_maps_file${renombrado} >> $smtp_generic_maps_file

postmap $smtp_generic_maps_file
