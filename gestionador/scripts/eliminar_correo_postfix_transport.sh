#!/bin/bash
# Le pasamos el correo como argumento. Nos eliminara el correo.
transport_maps_file='/etc/postfix/transport'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $transport_maps_file $transport_maps_file${renombrado}

n_linea=0
n_linea_encontrada=0
texto_borrar=$(cat $transport_maps_file | grep "$1" )
#| cut -d" " -f1)

while read line
        do
                n_linea=$((n_linea+1))
                if [ "$line" = "$texto_borrar" ]; then
                        n_linea_encontrada=$n_linea
			#echo "encontrado"

                fi

        done < $transport_maps_file

#echo $texto_borrar
#echo $n_linea_encontrada
cat $transport_maps_file | sed "$n_linea_encontrada,$n_linea_encontrada d" > $transport_maps_file-tmp
mv $transport_maps_file-tmp $transport_maps_file

postmap $transport_maps_file
