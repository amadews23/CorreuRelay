/*
# Archivo: comprobaciones.js
# Autor: Bartolomé Vich Lozano
# Email: amadews23@hotmail.com
# Fecha: 3 de Diciembre de 2019
# Descripción: Verificaciones de campos, nombre de usuario, password y correo electrónico.  
*/
function verificar_texto_espacios(t1, texto) {
	var noValido = /\s/;
	texto.style.color = "red";
	if(noValido.test(t1)){ 
		alert ("No puede contener espacios en blanco."); 
		texto.innerHTML="El cuadro de texto no puede contener espacios en blanco.";
		return false; 
	} 
    	return true;
}

function verificar_texto_tamanyo(t1, tamanyo, texto) {
	var espacios = false;
	texto.style.color = "red";
    	if (t1.length < tamanyo ) {
      		alert("Debe contener mínimo "+tamanyo+" caracteres.");
		texto.innerHTML="Escriba mínimo "+tamanyo+" caracteres para el cuadro de texto.";
      		return false;
    	}
	texto.innerHTML="";
      	return true; 
}
function verificar_direccion_correo(t1, texto) {

	var regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	texto.style.color = "red";
	if(regex.test(t1) ) {
		return true;
	} else {
	      	alert("Escriba una dirección de correo válida.");
		texto.innerHTML="Escriba una dirección de correo válida para el cuadro de texto.";
		return false;
	}
}
function verificar_usuario() {
	var t1 = document.getElementById("usuario").value;
	var texto = document.getElementById("usuario_text");

	if ( verificar_texto_tamanyo(t1, 4, texto) && verificar_texto_espacios(t1, texto) ) {
		return true;
	} 
	return false; 

}
function verificar_correo() {
	var t1 = document.getElementById("correo").value;
	var texto = document.getElementById("correo_text");

	if ( verificar_direccion_correo(t1, texto) && verificar_texto_tamanyo(t1, 8, texto) ) {
		return true;
	} 
	return false;

}
function verificar_password(p1, p2, texto) {
	texto.style.color = "red";
    	if (p1 != p2) {
      		alert("El password debe coincidir");
		texto.innerHTML="Los passwords deben coincidir.";
      		return false;
    	} else {    		
    		if (p1.length == 0 || p2.length == 0) {
      			alert("El password no puede estar vacio.");
			texto.innerHTML="El password no puede estar vacio.";
      			return false;
    		}
    		if (p1.length < 8 || p2.length < 8) {
      			alert("El password debe contener mínimo 8 caracteres.");
			texto.innerHTML="Escriba mínimo 8 caracteres.";
      			return false;
    		}
		texto.innerHTML="";
     		return true; 
    	}	
}

function verificar_password_usuario() {
	var p1 = document.getElementById("usuario_password1").value;
	var p2 = document.getElementById("usuario_password2").value;
	var texto = document.getElementById("usuario_password_text");
	if ( verificar_password(p1, p2, texto) == true ) {
		return true;
	}
	return false; 
}
	
function verificar_password_correo() {
	var p1 = document.getElementById("correo_password1").value;
	var p2 = document.getElementById("correo_password2").value;
	var texto = document.getElementById("correo_password_text");

	if ( verificar_password(p1, p2, texto) == true ) {
		return true;
	}
	return false; 
}

function verificar_todo() {

	if ( verificar_usuario() && verificar_password_usuario() && verificar_correo() && verificar_password_correo()) {
		return true;
	} 
	return false;
}
