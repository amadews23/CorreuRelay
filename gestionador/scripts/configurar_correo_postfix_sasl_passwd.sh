#!/bin/bash

#sasl_password_file='/etc/postfix/sasl/sasl_passwd'
sasl_password_file='sasl_passwd'
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $sasl_password_file $sasl_password_file${renombrado}

echo $1'	'$1':'$2 > $sasl_password_file
cat $sasl_password_file${renombrado} >> $sasl_password_file
#postmap ${sasl_password_file}
