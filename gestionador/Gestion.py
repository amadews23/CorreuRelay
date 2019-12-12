#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import model
import comprobar_usuario
import comprobar_correo
import crear_usuario
import configurar_correo
import administrar_servicios
import modificar_usuario
import modificar_correo
import eliminar_cuenta

urls = (
    '/', 'Listar',
    '/login', 'Login',
    '/logout', 'Logout',
    '/eliminar', 'Eliminar',
    '/eliminar_cuenta', 'EliminarCuenta',
    '/eliminar_correo', 'EliminarCorreo',
    '/modificar', 'Modificar',
    '/modificar_usuario', 'ModificarUsuario',
    '/modificar_usuario_password', 'ModificarUsuarioPassword',
    '/modificar_correo', 'ModificarCorreo',
    '/modificar_correo_password', 'ModificarCorreoPassword',
    '/crear', 'Crear',
    '/crear_cuenta', 'CrearCuenta',
)

web.config.debug = False
render = web.template.render('templates', base='base')
render2 = web.template.render('templates', base='base2')
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

class Login:

    login_form = web.form.Form( web.form.Textbox('username', web.form.notnull),
        web.form.Password('password', web.form.notnull),
        web.form.Button('Login'),
        )

    def GET(self):
        formulario = self.login_form()
        return render.login(formulario)

    def POST(self):
        if not self.login_form.validates():
            return render.login(self.login_form)
        
        username = self.login_form['username'].value
        password = self.login_form['password'].value
	usuario_valido = None
	password_valido = None
	verificado = None

        usuario_sesion = model.get_usuario(username)
	
	for a in usuario_sesion:
		usuario_valido = a.usuario
		password_valido = a.password
		
	if username == usuario_valido and password == password_valido:
		session.logged_in = True
        	raise web.seeother('/')
	else:
		verificado = "Usuario o password no validos"

        return render.login(self.login_form, verificado)

class Logout:

    def GET(self):
	print "INFO: Cerrada sesion"
        session.logged_in = False
        raise web.seeother('/')

class Listar:

    def GET(self):
        if session.get('logged_in', False):
            cuentas = model.get_cuentas()
            return render2.listar(cuentas)
	
        else:
            raise web.seeother('/login')

class Eliminar:

    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		return render2.eliminar(data.usuario, data.correo)
        else:
            raise web.seeother('/login')

class EliminarCuenta:

    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		eliminar_cuenta.eliminar_correo(data.correo, data.usuario)
		administrar_servicios.reiniciar_servicios_todos()
		'''Si fetchmail NO se inicio bien'''
		if (administrar_servicios.reiniciar_servicio_fetchmail() == False):

			resultado = "ERROR: Fetchmail no se inicio correctamente. Pongase en contacto con el Administrador"
			return render2.eliminar_cuenta(data.usuario, data.correo, resultado)
		
		else:
			if (administrar_servicios.reiniciar_servicio_dovecot() == False):	
						
				resultado = "ERROR: Dovecot no se inicio correctamente. Pongase en contacto con el Administrador"
				return render2.eliminar_cuenta(data.usuario, data.correo, resultado)

			else:
				eliminar_cuenta.eliminar_usuario_unix(data.usuario)
				resultado = "La cuenta ha sido eliminada"
				model.del_cuentas(data.usuario)
				return render2.eliminar_cuenta(data.usuario, data.correo, resultado)
        else:
            raise web.seeother('/login')

class EliminarCorreo:

    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		eliminar_cuenta.eliminar_correo(data.correo, data.usuario)
		administrar_servicios.reiniciar_servicios_todos()
		'''Si fetchmail NO se inicio bien'''
		if (administrar_servicios.reiniciar_servicio_fetchmail() == False):

			resultado = "ERROR: Fetchmail no se inicio correctamente. Pongase en contacto con el Administrador"
			return render2.eliminar_correo(data.usuario, data.correo, resultado)
		
		else:
			if (administrar_servicios.reiniciar_servicio_dovecot() == False):	
						
				resultado = "ERROR: Dovecot no se inicio correctamente. Pongase en contacto con el Administrador"
				return render2.eliminar_correo(data.usuario, data.correo, resultado)

			else:
				resultado = "La cuenta ha sido eliminada"
				model.del_cuentas(data.usuario)
				return render2.eliminar_correo(data.usuario, data.correo, resultado)
		
        else:
            raise web.seeother('/login')

class Modificar:

    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		return render2.modificar(data.usuario, data.correo)
        else:
            raise web.seeother('/login')

class ModificarUsuario:
    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		if data.usuario == data.usuario0:
			resultado = "El nombre de Usuario que intenta modificar es el mismo que el actual"
			return render2.modificar_usuario_error(data.usuario, data.usuario0, data.correo, resultado)

		else:
			'''Si el usuario esta dado de alta en la base de datos no comprueba nada mas'''
			if comprobar_usuario.comprobar_usuario_bd(data.usuario) == True:
		
				resultado = "ERROR: el Usuario ya está dado de alta en la Base de Datos."
				return render2.modificar_usuario_error(data.usuario, data.usuario0, data.correo, resultado)
			else:

				'''Comprueba que el usuario exista en el sistema, si existe no continua'''
				if comprobar_usuario.comprobar_usuario_unix(data.usuario) == True:

					resultado = "ERROR: el Usuario ya existe en el Sistema."
					return render2.modificar_usuario_error(data.usuario, data.usuario0, data.correo, resultado)

				else:
					'''Aplicamos la modificacion de cambio de usuario unix, modificamos archivos en Fetchmail y Postfix'''
					modificar_usuario.modificar_usuario_sistema(data.usuario, data.usuario0, data.correo)
					'''Reiniciamos todos los servicios'''
					administrar_servicios.reiniciar_servicios_todos()
					'''Si fetchmail NO se inicio bien'''
					if (administrar_servicios.reiniciar_servicio_fetchmail() == False):

						resultado = "ERROR: Fetchmail no se inicio correctamente. Pongase en contacto con el Administrador"
						return render2.modificar_usuario_error(data.usuario, data.usuario0, data.correo, resultado)
		
					else:
						if (administrar_servicios.reiniciar_servicio_dovecot() == False):	
						
							resultado = "ERROR: Dovecot no se inicio correctamente. Pongase en contacto con el Administrador"
							return render2.modificar_usuario_error(data.usuario, data.usuario0, data.correo, resultado)

						else:							
							resultado = "El usuario se modifico correctamente."
							model.upd_cuentas_usuario(data.usuario, data.usuario0)
							return render2.modificar_usuario(data.usuario, data.usuario0, data.correo)

        else:
            raise web.seeother('/login')

class ModificarUsuarioPassword:
    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()
		modificar_usuario.modificar_usuario_password(data.usuario, data.usuario_password1)
		resultado = "Ha sido modificado."
		return render2.modificar_usuario_password(data.usuario, resultado, data.correo)
        else:
            raise web.seeother('/login')

class ModificarCorreo:
    def POST(self):

        if session.get('logged_in', False):
        	data = web.input()
		if data.correo == data.correo0:
			resultado = "El nombre de la cuenta de correo que intenta modificar es el mismo que el actual"
			return render2.modificar_correo_error(data.correo, data.correo0, data.usuario, resultado)

		else:
			'''Comprueba que si el correo NUEVO esta dado de alta en la base de datos, si existe no continua'''
			if comprobar_correo.comprobar_correo_bd(data.correo) == True:

				resultado = "ERROR: la cuenta de Correo ya está dada de alta en la Base de Datos."
				return render2.modificar_correo_error(data.correo, data.correo0, data.usuario, resultado)

			else:
					
				'''Si el correo NUEVO esta configurado Postfix y Fetchmail, no sigue'''					
				if comprobar_correo.comprobar_correo_existe(data.correo) == True:

					resultado = "ERROR: la cuenta de Correo ya está configurada en el Sistema."
					return render2.modificar_correo_error(data.correo, data.correo0, data.usuario, resultado)					
				else:

					modificar_correo.modificar_correo_sistema(data.correo, data.correo0, data.usuario)
					administrar_servicios.reiniciar_servicios_todos()

					'''Si fetchmail NO se inicio bien'''
					if (administrar_servicios.reiniciar_servicio_fetchmail() == False):

						resultado = "ERROR: Fetchmail no se inicio correctamente. Pongase en contacto con el Administrador"
						return render2.modificar_correo_error(data.correo, data.correo0, data.usuario, resultado)
		
					else:
						if (administrar_servicios.reiniciar_servicio_dovecot() == False):	
						
							resultado = "ERROR: Dovecot no se inicio correctamente. Pongase en contacto con el Administrador"
							return render2.modificar_correo_error(data.correo, data.correo0, data.usuario, resultado)

						else:
						        resultado = "El correo se modifico correctamente."
							model.upd_correo(data.correo, data.correo0)
							return render2.modificar_correo(data.correo, data.correo0, data.usuario)
			
        else:
            raise web.seeother('/login')

class ModificarCorreoPassword:
    def POST(self):
        if session.get('logged_in', False):
        	data = web.input()

		administrar_servicios.reiniciar_servicios_todos()
		if (administrar_servicios.reiniciar_servicio_fetchmail() == False):

			resultado = "ERROR: Fetchmail no se inicio correctamente. Pongase en contacto con el Administrador"
			return render2.modificar_correo_password(data.correo, resultado, data.usuario)
		
		else:
			if (administrar_servicios.reiniciar_servicio_dovecot() == False):	
						
				resultado = "ERROR: Dovecot no se inicio correctamente. Pongase en contacto con el Administrador"
				return render2.modificar_correo_password(data.correo, resultado, data.usuario)

			else:
				resultado = "Ha sido modificado."
				return render2.modificar_correo_password(data.correo, resultado, data.usuario)
        else:
            raise web.seeother('/login')

class Crear:

    def GET(self):
        if session.get('logged_in', False):
        	data = web.input()
		return render2.crear()
        else:
            raise web.seeother('/login')

class CrearCuenta:

    def POST(self):
        if session.get('logged_in', False):

        	data = web.input()

		'''Si el usuario esta dado de alta en la base de datos no comprueba nada mas'''
		if comprobar_usuario.comprobar_usuario_bd(data.usuario) == True:

			resultado = "ERROR: el Usuario ya está dado de alta en la Base de Datos."
			return render2.crear_cuenta_error(data.correo, resultado, data.usuario)

		else:

			'''Comprueba que el usuario exista en el sistema, si existe no continua'''
			if comprobar_usuario.comprobar_usuario_unix(data.usuario) == True:

				resultado = "ERROR: el Usuario ya existe en el Sistema."
				return render2.crear_cuenta_error(data.correo, resultado, data.usuario)

			else:

				'''Comprueba que si el correo esta dado de alta en la base de datos, si existe no continua'''
				if comprobar_correo.comprobar_correo_bd(data.correo) == True:

					resultado = "ERROR: la cuenta de Correo ya está dada de alta en la Base de Datos."
					return render2.crear_cuenta_error(data.correo, resultado, data.usuario)

				else:
					
					'''Si el correo esta configurado Postfix y Fetchmail, no sigue'''					
					if comprobar_correo.comprobar_correo_existe(data.correo) == True:

						resultado = "ERROR: la cuenta de Correo ya está configurada en el Sistema."
						return render2.crear_cuenta_error(data.correo, resultado, data.usuario)
					else:

						'''Creamos usuario unix + passw'''
						crear_usuario.crear_usuario_unix(data.usuario, data.usuario_password1)

						if comprobar_usuario.comprobar_usuario_unix(data.usuario) == False:

							resultado = "ERROR: el Usuario no fue creado"		
							return render2.crear_cuenta_error(data.correo, resultado, data.usuario)					
						else:
							
							print "INFO: El usuario se creó correctamente."
	
							'''Configuramos los archivos del servicio de correo'''
							configurar_correo.configurar_correo(data.correo, data.correo_password1, data.usuario)
							
							'''Reiniciamos servicios'''
							print "INFO: reiniciando servicios..."
							administrar_servicios.reiniciar_servicios_todos()

							'''Comprobamos servicios REVISAR no comprobar Postfix'''
							if administrar_servicios.comprobar_servicio_fetchmail() == False:
							
								print "ERROR: Fetchmail no se inicio correctamente"
								resultado = "ERROR: Algún servicio no se inicio correctamente. Pongase en contacto con el Administrador"
								return render2.crear_cuenta_error(data.correo, resultado, data.usuario)
			
							else:
								if administrar_servicios.comprobar_servicio_fetchmail() == False:
							
									print "ERROR: Fetchmail no se inicio correctamente"
									resultado = "ERROR: Algún servicio no se inicio correctamente. Pongase en contacto con el Administrador"
									return render2.crear_cuenta_error(data.correo, resultado, data.usuario)

								else:	

									print "INFO: Los servicios se reiniciaron correctamente"
									'''Insertamos en la BD'''
									model.new_cuentas(usuari, correu)
									print "INFO: La cuenta ha sido creada correctamente"	
									resultado = "La cuenta ha sido creada con exito."	
									return render2.crear_cuenta(data.correo, resultado, data.usuario)
        else:
            raise web.seeother('/login')


app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session

if __name__ == '__main__':
    app.run()
