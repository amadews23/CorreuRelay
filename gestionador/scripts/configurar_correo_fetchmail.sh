#!/bin/bash
#fetchmailrc_file='/etc/fetchmailrc'
fetchmailrc_file='fetchmailrc'
pop_remoto='pop3.strato.com'

renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old

#Realizamos copia por si algo sale mal
cp $fetchmailrc_file $fetchmailrc_file${renombrado}
echo ' ' >> $fetchmailrc_file
echo 'poll '$pop_remoto >> $fetchmailrc_file
echo '	proto POP3' >> $fetchmailrc_file
echo '	user '$1 >> $fetchmailrc_file
echo '	pass '$2 >> $fetchmailrc_file
echo '	ssl' >> $fetchmailrc_file
echo '	sslcertck' >> $fetchmailrc_file
echo 'to '$3 >> $fetchmailrc_file
echo '' >> $fetchmailrc_file
