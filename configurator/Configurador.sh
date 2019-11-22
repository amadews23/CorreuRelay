#!/bin/bash
# Archivo: Configurar.sh
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 29 de Octubre de 2019
# Descripción: Instalador y configurador para Postfix, Dovecot-pop3, Fetchmail y otros paquetes 
mi_fqdn='CorreuServer.midominio.com'
smtp_remoto='smtp.midominio.com'
puerto_smtp_remoto=587
pop3_remoto='pop3.midominio.com'
usuario_unix="usuario"
directorio_home=$(eval echo ~$usuario_unix)
red_permitida='192.168.2.0/24'
cuenta_por_defecto='micorreo@midominio.com'
smtp_tls_CAfile_file='/etc/postfix/ca_cert.pem'
sasl_password_file='/etc/postfix/sasl/sasl_passwd'
sender_depend_relay_hostmaps_file='/etc/postfix/relay_hostmap'
transport_maps_file='/etc/postfix/transport'
smtp_generic_maps_file='/etc/postfix/generic'
mi_host=$(cat /etc/hostname)
frecuencia_descarga_fetchmail=150
postfix_configurar_antes() {
        debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet with smarthost'"
        debconf-set-selections <<< "postfix postfix/mailname string ${mi_fqdn}"
        debconf-set-selections <<< "postfix postfix/relayhost string [${smtp_remoto}]:submission"
}
instalar_sino_esta() {
        listar_paquete=$(dpkg-query -W -f='${Package}\n' | grep $paquete | head -n 1)
        if [ "$listar_paquete" == "$paquete" ]
        	then
          	echo "El paquete: $paquete, SI está instalado."
        else
          	echo -e "El paquete: $paquete, NO está instalado."
	  	echo "Instalando..."
                if [ "$paquete" == "postfix" ]
                        then
                        echo "postfix"
                        postfix_configurar_antes
                        fi
          apt-get install $paquete -y
        fi
}
postfix_configurar_main_cf() {
	#Realizamos una copia de main.cf por si algo sale mal
	cp /etc/postfix/main.cf /etc/postfix/main.cf-$(date +"%d-%h-%y_%H:%M:%S").old
	#Eliminamos del banner la version del S.O.
	postconf -e 'smtpd_banner = $myhostname ESMTP'
	postconf -e 'smtp_sasl_auth_enable = yes'
	postconf -e "smtp_sasl_password_maps = hash:$sasl_password_file"
	postconf -e 'smtp_sasl_security_options = noanonymous'
	postconf -e "smtp_tls_CAfile = $smtp_tls_CAfile_file"
	postconf -e 'smtp_use_tls = yes'
	redes=$(postconf -d mynetworks | awk '{$1=$2="";print $0}')
	postconf -e "mynetworks = $redes $red_permitida"
	#cambiamos en postfix el tipo de buzon
	postconf -e 'home_mailbox = Maildir/'
	#relay_hostmap
	postconf -e "sender_depend_relayhost_maps = hash:$sender_depend_relay_hostmaps_file"
	#para recibir correo de manera local en nuestra red
	postconf -e "transport_maps = hash:$transport_maps_file"
	#para que el usuario pueda enviar desde la terminal
	postconf -e "smtp_generic_maps = hash:$smtp_generic_maps_file"
	#autenticacion
	postconf -e 'smtpd_sasl_type = dovecot'
	postconf -e 'smtpd_sasl_path = private/auth'
	postconf -e 'smtpd_sasl_auth_enable = yes'
	#obligar a autenticar
	postconf -e 'smtpd_client_restrictions = permit_sasl_authenticated, reject'
	postconf -e 'smtpd_recipient_restrictions = permit_sasl_authenticated, reject_unauth_destination' 
}
postfix_copiar_certificado() {
	cp /etc/ssl/certs/thawte_Primary_Root_CA.pem ${smtp_tls_CAfile_file}
}
pedir_password() {
	read -s password_1
	echo "repita la contrasenya"
	read -s password_2
}
postfix_configurar_sasl_passwd() {
	if [ -f "$sasl_password_file" ]; then
    		echo "$sasl_password_file existe, realizando copia"
		#copiamos por si algo sale mal
		cp ${sasl_password_file} ${sasl_password_file}-$(date +"%d-%h-%y_%H:%M:%S").old
	fi
	echo "Introduzca la contrasenya de ${cuenta_por_defecto}"
	pedir_password
	while [ $password_1 != $password_2 ]; do
		echo "Haga el favor de poner bien la contrasenya para ${cuenta_por_defecto}"
		pedir_password
	done
	echo "[${smtp_remoto}]:${puerto_smtp_remoto} ${cuenta_por_defecto}:${password_1}" > ${sasl_password_file}
	postmap ${sasl_password_file}
	#permisos para que no pueda ser leido que no sea root
	chmod 660 ${sasl_password_file} 
}
postfix_configurar_sender_depend_relay_hostmaps() {
        if [ -f "$sender_depend_relay_hostmaps_file" ]; then
                echo "$sender_depend_relay_hostmaps_file existe, realizando copia"
                #copiamos por si algo sale mal
                cp ${sender_depend_relay_hostmaps_file} ${sender_depend_relay_hostmaps_file}-$(date +"%d-%h-%y_%H:%M:%S").old
        fi
	echo "${cuenta_por_defecto} [${smtp_remoto}]:${puerto_smtp_remoto}" > ${sender_depend_relay_hostmaps_file}
	postmap ${sender_depend_relay_hostmaps_file}
}
postfix_configurar_transport_maps() {
        if [ -f "$transport_maps_file" ]; then
                echo "$transport_maps_file existe, realizando copia"
                #copiamos por si algo sale mal
                cp ${transport_maps_file} ${transport_maps_file}-$(date +"%d-%h-%y_%H:%M:%S").old
        fi
        echo "${cuenta_por_defecto} local" > ${transport_maps_file}
	echo "*		smtp:[${smtp_remoto}]:${puerto_smtp_remoto}" >> ${transport_maps_file}
	postmap ${transport_maps_file}
}
postfix_configurar_smtp_generic_maps_file() {
        if [ -f "$smtp_generic_maps_file" ]; then
                echo "$smtp_generic_maps_file existe, realizando copia"
                #copiamos por si algo sale mal
                cp ${smtp_generic_maps_file} ${smtp_generic_maps_file}-$(date +"%d-%h-%y_%H:%M:%S").old
        fi
        echo "${usuario_unix}@${mi_host}	${cuenta_por_defecto}" > ${smtp_generic_maps_file}
	postmap ${smtp_generic_maps_file}
}
dovecot_configurar_dovecot_conf() {
	echo "/etc/dovecot/dovecot.conf, realizando copia"
	renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
	cp /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf${renombrado}
	python sustituir_texto.py -s /etc/dovecot/dovecot.conf${renombrado} -o /etc/dovecot/dovecot.conf -p1 '#listen = *, ::' -t1 'listen = *, ::'
	echo "# Outlook Express y Windows Mail trabajan con LOGIN mechanism, no con el estandar PLAIN " >> /etc/dovecot/dovecot.conf
	echo "auth_mechanisms = plain login" >> /etc/dovecot/dovecot.conf
}
dovecot_configurar_10_auth_conf() {
        echo "/etc/dovecot/conf.d/10-auth.conf, realizando copia"
        renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
        cp /etc/dovecot/conf.d/10-auth.conf /etc/dovecot/conf.d/10-auth.conf${renombrado}
        python sustituir_texto.py -s /etc/dovecot/conf.d/10-auth.conf${renombrado} -o /etc/dovecot/conf.d/10-auth.conf -p1 '#disable_plaintext_auth = yes' -t1 'disable_plaintext_auth = no' -p2 'auth_mechanisms = plain' -t2 'auth_mechanisms = plain login'
}
dovecot_configurar_10_mail_conf() {
        echo "/etc/dovecot/conf.d/10-mail.conf, realizando copia"
        renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
        cp /etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/10-mail.conf${renombrado}
        python sustituir_texto.py -s /etc/dovecot/conf.d/10-mail.conf${renombrado} -o /etc/dovecot/conf.d/10-mail.conf -p1 'mail_location = mbox:~/mail:INBOX=/var/mail/%u' -t1 'mail_location = maildir:~/Maildir'
}
dovecot_configurar_10_master_conf() {
        echo "/etc/dovecot/conf.d/10-master.conf, realizando copia"
        renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
	cp /etc/dovecot/conf.d/10-master.conf /etc/dovecot/conf.d/10-master.conf${renombrado}
	lineas=$( echo -e "\tunix_listener /var/spool/postfix/private/auth { \n\t mode = 0666 \n\t user = postfix \n\t group = postfix \n }\n ")
	python sustituir_texto.py -s /etc/dovecot/conf.d/10-master.conf${renombrado} -o /etc/dovecot/conf.d/10-master.conf -p1 '  #unix_listener /var/spool/postfix/private/auth {' -t1 "$lineas"
}
cambiar_a_Maildir() {
	if [[ $(python existe_texto.py -s /etc/profile -p 'export MAIL=$HOME/Maildir') = 0 ]]; then 
        	echo "/etc/profile, realizando copia"
        	renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
        	cp /etc/profile /etc/profile${renombrado}
		echo 'export MAIL=$HOME/Maildir' >> /etc/profile
	fi
}
crear_skel_Maildir() {
	if [ -d '/etc/skel/Maildir/' ]; then
		echo "/etc/skel/Maildir, existe"
	else
		echo "/etc/skel/Maildir, no existe, creando"
		maildirmake.dovecot /etc/skel/Maildir
	fi
        if [ -d '/etc/skel/Maildir/.Drafts' ]; then
                echo "/etc/skel/Maildir/.Drafts, existe"
        else
                echo "/etc/skel/Maildir/.Drafts, no existe, creando"
                maildirmake.dovecot /etc/skel/Maildir/.Drafts
        fi
        if [ -d '/etc/skel/Maildir/.Sent' ]; then
                echo "/etc/skel/Maildir/.Sent, existe"
        else
                echo "/etc/skel/Maildir/.Sent, no existe, creando"
                maildirmake.dovecot /etc/skel/Maildir/.Sent
        fi
        if [ -d '/etc/skel/Maildir/.Trash' ]; then
                echo "/etc/skel/Maildir/.Trash, existe"
        else
                echo "/etc/skel/Maildir/.Trash, no existe, creando"
                maildirmake.dovecot /etc/skel/Maildir/.Trash
        fi
        if [ -d '/etc/skel/Maildir/.Templates' ]; then
                echo "/etc/skel/Maildir/.Templates, existe"
        else
                echo "/etc/skel/Maildir/.Templates, no existe, creando"
                maildirmake.dovecot /etc/skel/Maildir/.Templates
        fi

}
copiar_skel_Maildir() {
        if [ -d '$directorio_home/Maildir' ] && [ -d '$directorio_home/Maildir/.Drafts' ] && [ -d '$directorio_home/Maildir/.Sent' ] && [ -d '$directorio_home/Maildir/.Trash' ] && [ -d '$directorio_home/Maildir/.Templates' ]  ; then
                echo "$directorio_home/Maildir/, existe"
        else
                echo "$directorio_home/Maildir/, no existe, copiando /etc/skel/Maildir/"
                cp -r /etc/skel/Maildir $directorio_home
		chown -R $usuario_unix:$usuario_unix $directorio_home/Maildir
		chmod -R 700 $directorio_home/Maildir
        fi

}
fetchmail_configurar_etc_fetchmailrc() {
        if [ -f '/etc/fetchmailrc' ]; then
		echo "/etc/fetchmailrc existe, creando copia"
		cp /etc/fetchmailrc /etc/fetchmailrc-$(date +"%d-%h-%y_%H:%M:%S").old
	fi
	echo 'set logfile "/var/log/fetchmail.log"' > /etc/fetchmailrc
	echo 'set postmaster "postmaster"' >> /etc/fetchmailrc
	echo "set daemon $frecuencia_descarga_fetchmail" >> /etc/fetchmailrc
	echo ' ' >> /etc/fetchmailrc
	echo 'defaults' >> /etc/fetchmailrc
	echo '	pass8bits' >> /etc/fetchmailrc
 	echo '	keep' >> /etc/fetchmailrc #Deja los mensajes en el servidor remoto
	#TODO revisar para si distinto home:
	echo '	mda "HOME=/home/%T /usr/bin/sudo -u %T /usr/lib/dovecot/deliver"' >> /etc/fetchmailrc
	echo "poll $pop3_remoto" >> /etc/fetchmailrc
	echo '	proto POP3' >> /etc/fetchmailrc
	echo "	user $cuenta_por_defecto" >> /etc/fetchmailrc
	echo "	pass $password_1" >> /etc/fetchmailrc
	echo '	ssl' >> /etc/fetchmailrc
	echo '	sslcertck' >> /etc/fetchmailrc
	echo "to $usuario_unix" >> /etc/fetchmailrc
	chmod 600 /etc/fetchmailrc
}
fetchmail_configurar_etc_default_fetchmail() {
        echo "/etc/default/fetchmail, realizando copia"
        renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
        cp /etc/default/fetchmail /etc/default/fetchmail${renombrado}
        python sustituir_texto.py -s /etc/default/fetchmail${renombrado} -o /etc/default/fetchmail -p1 'START_DAEMON=no' -t1 'START_DAEMON=yes '
	echo "" >> /etc/default/fetchmail
}
sudoers_configurar() {
	if [[ $(python existe_texto.py -s /etc/sudoers -p 'fetchmail ALL=(ALL) NOPASSWD:/usr/lib/dovecot/deliver') = 0 ]]; then 
        	echo "/etc/sudoers, realizando copia"
        	renombrado=-$(date +"%d-%h-%y_%H:%M:%S").old
        	cp /etc/sudoers /etc/sudoers${renombrado}
		echo "fetchmail ALL=(ALL) NOPASSWD:/usr/lib/dovecot/deliver" >> /etc/sudoers
	fi
}
paquete="postfix"
instalar_sino_esta
paquete="fetchmail"
instalar_sino_esta
paquete='net-tools'
instalar_sino_esta
paquete='sudo'
instalar_sino_esta
paquete='dovecot-pop3d'
instalar_sino_esta
#configuramos Postfix
postfix_configurar_main_cf
postfix_configurar_sasl_passwd
postfix_configurar_sender_depend_relay_hostmaps
postfix_configurar_transport_maps
postfix_configurar_smtp_generic_maps_file
postfix_copiar_certificado
#configuramos Dovecot
dovecot_configurar_dovecot_conf
dovecot_configurar_10_auth_conf
dovecot_configurar_10_mail_conf
dovecot_configurar_10_master_conf
#cambiar buzones de mbox a Maildir
cambiar_a_Maildir
#Crear skeleton
crear_skel_Maildir
#Copiar en usuario
copiar_skel_Maildir
#configuramos Fetchmail
fetchmail_configurar_etc_fetchmailrc
fetchmail_configurar_etc_default_fetchmail
sudoers_configurar
chmod a+rwxt /var/mail
service postfix restart
service dovecot restart
service fetchmail restart
