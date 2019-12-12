#!/bin/bash
# Le pasamos el correo como argumento. Nos eliminara el pool que contiene usuario y correo.
#fetchmailrc_file='/etc/fetchmailrc'
fetchmailrc_file='fetchmailrc'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $fetchmailrc_file $fetchmailrc_file${renombrado}

n_linea=0
n_linea_encontrada=0
while read line
        do
                n_linea=$((n_linea+1))
                if [ "$line" = "user $1" ]; then
                        n_linea_encontrada=$n_linea
                fi

        done < $fetchmailrc_file

#echo $n_linea_encontrada
n_primera_linea_borrar=$((n_linea_encontrada-2))
n_ultima_linea_borrar=$((n_linea_encontrada+4))
#echo $n_primera_linea_borrar $n_ultima_linea_borrar 

cat $fetchmailrc_file | sed "$n_primera_linea_borrar,$n_ultima_linea_borrar d" > $fetchmailrc_file-tmp
mv $fetchmailrc_file-tmp $fetchmailrc_file
