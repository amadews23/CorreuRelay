#!/bin/bash
fetchmailrc_file='/etc/fetchmailrc'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')

#Realizamos copia por si algo sale mal
cp $fetchmailrc_file $fetchmailrc_file${renombrado}

python sustituir_texto.py -s $fetchmailrc_file${renombrado} -o  $fetchmailrc_file -p1 "to $2" -t1 "to $1  ${salto}"
