#!/bin/bash
# Le pasamos el correo como argumento. Nos eliminara el correo.
#sender_depend_relay_hostmaps_file='/etc/postfix/relay_hostmap'
sender_depend_relay_hostmaps_file='relay_hostmap'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $sender_depend_relay_hostmaps_file $sender_depend_relay_hostmaps_file${renombrado}

n_linea=0
n_linea_encontrada=0
texto_borrar=$(cat $sender_depend_relay_hostmaps_file | grep $1 )
#| cut -d" " -f1)

while read line
        do
                n_linea=$((n_linea+1))
                if [ "$line" = "$texto_borrar" ]; then
                        n_linea_encontrada=$n_linea
			#echo "encontrado"

                fi

        done < $sender_depend_relay_hostmaps_file


#echo $n_linea_encontrada
cat $sender_depend_relay_hostmaps_file | sed "$n_linea_encontrada,$n_linea_encontrada d" > $sender_depend_relay_hostmaps_file-tmp
mv $sender_depend_relay_hostmaps_file-tmp $sender_depend_relay_hostmaps_file

#postmap ${sender_depend_relay_hostmaps_file}
