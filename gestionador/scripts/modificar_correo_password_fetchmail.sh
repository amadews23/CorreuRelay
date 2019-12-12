#!/bin/bash
fetchmailrc_file='/etc/fetchmailrc'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
salto=$(echo -e '\n ')
salto2=$(echo -e '\r')
#Realizamos copia por si algo sale mal
cp $fetchmailrc_file $fetchmailrc_file${renombrado}

python sustituir_texto.py -s $fetchmailrc_file${renombrado} -o  $fetchmailrc_file -p1 "	user $1" -t1 "	userx ${salto2}"
python sustituir_texto.py -s $fetchmailrc_file -o  $fetchmailrc_file"-tmp" -p1 "	userx " -t1 "	user $1 ${salto}	pass $2${salto}"
mv $fetchmailrc_file"-tmp" $fetchmailrc_file
