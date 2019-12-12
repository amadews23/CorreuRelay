import web

db = web.database(dbn='sqlite', db='gestion.db')

def get_cuentas():
    
    return db.select('cuentas', what="cuentas.Id, cuentas.usuario, cuentas.correo")

def get_cuentas_usuarios():
    
    return db.select('cuentas', what="cuentas.usuario")

def get_cuentas_correos():
    
    return db.select('cuentas', what="cuentas.correo")

def new_cuentas(usuari, correu):
    db.insert('cuentas', usuario=usuari, correo=correu)

def upd_cuentas_usuario(usuari, usuari0):
    db.update('cuentas', where="cuentas.usuario=$usuari0", usuario=usuari ,vars=locals())  
	 
def del_cuentas(usuari):

    db.delete('cuentas', where="cuentas.usuario=$usuari", vars=locals())

def get_usuario(usuario):

    return db.select('usuarios', what="usuarios.usuario, usuarios.password", where="usuarios.usuario=$usuario", vars=locals())

