#!/bin/bash
# Le pasamos el usuario como argumento. Nos eliminara el correo local usuario@hotname y correo.
smtp_generic_maps_file='/etc/postfix/generic'

mi_host=$(cat /etc/hostname)
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $smtp_generic_maps_file $smtp_generic_maps_file${renombrado}

n_linea=0
n_linea_encontrada=0
texto_borrar=$(cat $smtp_generic_maps_file | grep "$1@$mi_host" )
#| cut -d" " -f1)

while read line
        do
                n_linea=$((n_linea+1))
                if [ "$line" = "$texto_borrar" ]; then
                        n_linea_encontrada=$n_linea
			#echo "encontrado"

                fi

        done < $smtp_generic_maps_file

#echo $texto_borrar
#echo $n_linea_encontrada
cat $smtp_generic_maps_file | sed "$n_linea_encontrada,$n_linea_encontrada d" > $smtp_generic_maps_file-tmp
mv $smtp_generic_maps_file-tmp $smtp_generic_maps_file

postmap ${smtp_generic_maps_file}
