#!/bin/bash

#sender_depend_relay_hostmaps_file='/etc/postfix/relay_hostmap'
sender_depend_relay_hostmaps_file='relay_hostmap'
smtp_remoto=smtp.strato.com
puerto_smtp_remoto=587
renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $sender_depend_relay_hostmaps_file $sender_depend_relay_hostmaps_file${renombrado}

echo $1' ['$smtp_remoto']:'$puerto_smtp_remoto > $sender_depend_relay_hostmaps_file
cat $sender_depend_relay_hostmaps_file${renombrado} >> $sender_depend_relay_hostmaps_file

#postmap ${sender_depend_relay_hostmaps_file}
