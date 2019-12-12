#!/bin/bash

#sender_depend_relay_hostmaps_file='/etc/postfix/relay_hostmap'
sender_depend_relay_hostmaps_file='relay_hostmap'
smtp_remoto=smtp.strato.com
puerto_smtp_remoto=587
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')

#Realizamos copia por si algo sale mal
cp $sender_depend_relay_hostmaps_file $sender_depend_relay_hostmaps_file${renombrado}

python sustituir_texto.py -s $sender_depend_relay_hostmaps_file${renombrado} -o  $sender_depend_relay_hostmaps_file -p1 "$2" -t1 "$1 [$smtp_remoto]:$puerto_smtp_remoto${salto}"

cat $sender_depend_relay_hostmaps_file | sed 's/^[[:space:]]*//' > $sender_depend_relay_hostmaps_file"-tmp"
#Renombramos temporal
mv $sender_depend_relay_hostmaps_file"-tmp" $sender_depend_relay_hostmaps_file

#postmap ${sender_depend_relay_hostmaps_file}

