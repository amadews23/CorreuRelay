#!/bin/bash
# Le pasamos el correo como argumento. Nos eliminara el correo.
sasl_password_file='/etc/postfix/sasl/sasl_passwd'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $sasl_password_file $sasl_password_file${renombrado}

n_linea=0
n_linea_encontrada=0
texto_borrar=$(cat $sasl_password_file | grep $1 )
#| cut -d" " -f1)

while read line
        do
                n_linea=$((n_linea+1))
                if [ "$line" = "$texto_borrar" ]; then
                        n_linea_encontrada=$n_linea
			#echo "encontrado"

                fi

        done < $sasl_password_file


#echo $n_linea_encontrada
cat $sasl_password_file | sed "$n_linea_encontrada,$n_linea_encontrada d" > $sasl_password_file-tmp
mv $sasl_password_file-tmp $sasl_password_file

postmap ${sasl_password_file}
