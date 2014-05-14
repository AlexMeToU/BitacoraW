# -*- coding: utf-8 *-*
#!/usr/bin/ python
'''
Created on 19/03/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
#import logging
from datetime import datetime
import pygame
from pygame.locals import *
import sys
sys.path.append("..")
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import Clases.eztext
import Login.controller
import Login.LoginView
import InterfazUsuario.controller
import InterfazUsuario.UserView
import Asistencia.controller
import Asistencia.AttendanceView
# ------------------------------
# Funcion principal de la Aplicacion
# ------------------------------
"Vista de La Aplicacion para llevar un control de los Alumnos y los Equipos en las Aulas"
 
class vista():
     
    def main(self):
        "Metodo Main Principal"
        # Obtenemos el S.O Esto es para pruebas en Windows.
        sistemaop = sys.platform
        print sistemaop
        
        # Numero de Version Para los Modulos Integrados
        self.modulo_asistencia = False
        
        # Cargamos todo lo relacionado a pygame
        pygame.init()
        
        # Creamos las Instancias a los Controladores
        self.controlador = Login.controller.controlador()
        self.user_controlador = InterfazUsuario.controller.controlador()
        self.asist_controlador = Asistencia.controller.controlador()
        
        # Creamos las Instancias a las Vistas
        self.loginview = Login.LoginView.LoginView(sistemaop,self.modulo_asistencia)
        self.userview = InterfazUsuario.UserView.UserView(sistemaop,self.modulo_asistencia)
        self.asistview = Asistencia.AttendanceView.AttendanceView(sistemaop,self.modulo_asistencia)
        
        # Creamos la Ventana Login
        self.loginview.crear_interfaz()

        # create the pygame clock
        self.clock = pygame.time.Clock()
    
    """---------------------------------------Metodos-------------------------------------------------------"""
    
    def iniciar(self):
        "Metodo para El bucle Principal de la Aplicacion"
        # Si el SO es win Matamos al Explorer y Ejecutamos el Proceso Monitor_Controller
        self.controlador.Iniciar_Procesos()
        
        # Bandera para permitir escritura en los TextBox
        band_write = 1
        
        # Bandera para el acceso al equipo
        band_access = False
        
        # Bandera para el acceso a registrar Asistencia
        band_asist = False
        
        # Deshabilitamos elementos de Windows
        self.controlador.Deshabilitar_elementos_windows()
        
        # se muestran lo cambios en pantalla
        # el bucle principal del juego
        while True:
            # Nos Aseguramos que el codigo corre a 30 fps
            self.clock.tick(30)
            
            # Empezamos a capturar la lista de Eventos
            events = pygame.event.get()
                        
            for event in events:
                if band_access == False:
                    (band_write,band_access) = self.eventos_login(event,band_write,band_access)
                elif band_access == True:
                    if band_asist == False:
                        (band_access,band_asist) = self.eventos_userview(event,band_access,band_asist)
                    else:
                        band_asist = self.eventos_asistview(event,band_asist)

            if band_write == 1:
                # Se ingresan datos en el TextBox del Usuario
                self.loginview.usuario.update(events)
            elif band_write == 2:
                # Se ingresan datos en el TextBox del Pwd
                self.loginview.pwd.update(events)

            if band_access == False:
                # Se muestran los Surfaces de la Ventana Login
                self.loginview.surface()

                # refresh the display
                self.loginview.refresh_display()
            elif band_access == True:
                band_write = 1
                if band_asist == False:
                    self.userview.surface(self.user_controlador.get_user_type())
    
                    # refresh the display
                    self.userview.refresh_display()
                else:
                    if self.modulo_asistencia == True:
                        self.asistview.surface()
        
                        # refresh the display
                        self.asistview.refresh_display()

    def ingresar_sistema(self):
        "Metodo para El Ingreso del Usuario"
        # Se valida el Usuario ingresado
        res = self.controlador.Iniciar_Sesion(self.loginview.usuario.getTxt(), self.loginview.pwd.getTxt())
        # Si el usuario es el Admin se cierra la Aplicacion
        if res == "super":
            "Usuario Super"
            # Habilitamos Elementos de Windows
            self.controlador.Habilitar_elementos_windows()
            sys.exit(0)
        elif res == "SUCCESS_QUERY_REGISTER":
            # Si el Usuario es valido y se realizo el registro de sesion se cambia la Interfaz a la de Usuario
            "Usuario Valido"
            # Habilitamos Elementos de Windows
            self.controlador.Habilitar_elementos_windows()
            #logging.info('Se Inicio Sesion')            
            band_access = True
            # Pasamos la Informacion del usuario Logeado al Controlador del Usuario
            self.user_controlador.set_usuario(self.controlador.obtener_usuario_logeado())
            self.asist_controlador.set_usuario(self.controlador.obtener_usuario_logeado())
        elif res == "USER_NO_VALIDO":
            # Si el Usuario no es valido se manda mensaje a la Ventana
            "Usuario no valido"
            band_access = False
            self.loginview.mensaje.update_prompt("Usuario o Pwd no valido")
        elif res == "FAILED_VALIDATE":
            # Fallo Al realizar la Consulta
            "Fallo en Realizar Consulta"
            band_access = False
            self.loginview.mensaje.update_prompt("No se puede Consultar el Usuario")
        elif res == "FAILED_GET_IP":
            # Fallo Al Obtener la IP del Equipo
            "Fallo Al Obtener la IP del Equipo"
            band_access = False
            self.loginview.mensaje.update_prompt("IP No Valida")
        elif res == "FAILED_GET_HOUR":
            # Fallo Al Obtener la Hora del Servidor
            "Fallo Al Obtener la IP del Equipo"
            band_access = False
            self.loginview.mensaje.update_prompt("Hora No Valida")
        elif res == "FAILED_QUERY_REGISTER":
            # Fallo en Realizar Registro de Inicio de Sesion
            "Fallo en Realizar Registro de Inicio de Sesion"
            band_access = False
            self.loginview.mensaje.update_prompt("No se Realizo el Inicio de Sesion")
        return band_access
    
    def salir_sistema(self):
        "Metodo para La Salida del Usuario"
        res = self.user_controlador.registrar_Salida()
        if res == "SUCCESS_QUERY_REGISTER":
            # Reseteamos los TextBox del Login
            self.loginview.usuario.reset_input()
            self.loginview.pwd.reset_input()
            self.user_controlador.reset_usuario()
            self.controlador.Iniciar_Procesos()
            band_access = False
        elif res == "FAILED_GET_HOUR":
            # Fallo Al Obtener la Hora del Servidor
            "Fallo en Realizar Registro de Fin de Sesion"
            band_access = True
            self.userview.mensaje.update_prompt("Hora No Valida")
        elif res == "FAILED_QUERY_REGISTER":
            # Fallo en Realizar Registro de Fin de Sesion
            "Fallo en Realizar Registro de Fin de Sesion"
            band_access = True
            self.userview.mensaje.update_prompt("No se Realizo el Fin de Sesion")
        return band_access

    def clase_asistencia_alumno(self):
        "Metodo para Mostrar la Clase en la vista de Asistencia"
        self.asist_controlador.reset_asist_values()
        self.asistview.clase.update_prompt("Sin Clase")
        self.asistview.edo_asist.update_prompt("Sin Asistencia")
                
        (fecha_consulta,hora_consulta,dia,hora,minuto),edo_consulta = self.asist_controlador.Obtener_Hora_Fecha_Servidor()
        if edo_consulta == "SUCCESS":
            clase,res = self.asist_controlador.obtener_clase_alumno(fecha_consulta,dia,hora)
            if res == "FAILED_GET_GPO":
                self.asistview.mensaje.update_prompt("Grupo No Valido")
            elif res == "FAILED_GET_CLASS":
                self.asistview.mensaje.update_prompt("Clase No Valida")
            elif res == "FAILED_GET_MAT":
                self.asistview.mensaje.update_prompt("Materia No Valida")
            elif res == "FAILED_GET_HOUR":
                self.asistview.mensaje.update_prompt("Hora No Valida")
            else:
                self.asistview.clase.update_prompt(clase)
                self.asistview.mensaje.update_prompt(res)
                # Obtenemos el status de la Asistencia del Alumno
                asist,res = self.asist_controlador.obtener_asist_alum(fecha_consulta)
                if res == "FAILED_GET_ASIST":
                    self.asistview.mensaje.update_prompt("Edo. de Asistencia No Valido")
                else:
                    self.asistview.edo_asist.update_prompt(asist)
        else:
            self.asistview.mensaje.update_prompt("Hora no Valida")

        
    def registrar_asistencia(self):
        "Metodo para Registrar Asistencia del Usuario"
        (fecha_consulta,hora_consulta,dia,hora,minuto),edo_consulta = self.asist_controlador.Obtener_Hora_Fecha_Servidor()
        if edo_consulta == "SUCCESS":
            asistencia,res = self.asist_controlador.registrar_asistencia(fecha_consulta,hora_consulta,dia,hora,minuto)
            if res == "FAILED_GET_IP_ASIST":
                self.asistview.mensaje.update_prompt("IP no Valida")
            elif res == "SIN_CLASE":
                print "No se Hace Insercion en DB"
                self.asistview.mensaje.update_prompt("No hay Clase para Registrar Asistencia")
            elif res == "ASISTENCIA_FALTA":
                print "No se Hace Insercion en DB"
                self.asistview.mensaje.update_prompt("Tiempo excedido para Registrar Asistencia")
            elif res == "ASISTENCIA_DESTIEMPO":
                print "No se Hace Insercion en DB"
                self.asistview.mensaje.update_prompt("La Clase ya Finalizo para Registrar Asistencia")                
            elif res == "SIN_INSERCION":
                print "No se Hace Insercion en DB"
                self.asistview.mensaje.update_prompt("Ya se Tiene Registrada la Asistencia")
            else:
                self.asistview.edo_asist.update_prompt(asistencia)
                self.asistview.mensaje.update_prompt(res)

    """--------------------------------------Eventos-------------------------------------------------------"""

    def eventos_login(self,event,band_write,band_access):
        "Metodo para Los Eventos en la Vista Login"        
        if event.type == KEYDOWN:
            # Para iterar entre los dos TextBox de Usuario y Pwd
            if event.key == pygame.K_TAB:
                #print "Click en tecla TAB"
                if band_write < 2:
                    band_write += 1
                elif band_write == 2:
                    band_write = 1
            if event.key == K_KP_ENTER or event.key == K_RETURN:
                #Click en Tecla Enter
                band_access = self.ingresar_sistema()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Borramos Mensaje para el Usuario
            self.loginview.mensaje.update_prompt("")
                    
            # Dependiendo de la zona donde se hizo click se realiza una accion 
            x, y = event.pos
            # Si la Bandera == False se checan las surfaces del Login
            if band_access == False:
                if x>= 505 and x <= 755 and y >= 360 and y<= 385:
                    # Click en Textbox usuario
                    band_write = 1
                elif x>= 505 and x <= 755 and y >= 410 and y<= 440:
                    # Click en Textbox pwd
                    band_write = 2
                elif self.loginview.entrar.collidepoint(x, y):
                    # Click en Boton Entrar
                    band_access = self.ingresar_sistema()

                elif self.loginview.apagar.collidepoint(x, y):
                    # Click en Boton Apagar
                    self.controlador.ApagarEquipo()

        if band_access == True:
            self.userview.crear_interfaz()
            self.userview.usuario_logeado.update_prompt(self.user_controlador.get_name_user())

        return (band_write,band_access)

    def eventos_userview(self,event,band_access,band_asist):
        "Metodo para Los Eventos en la Vista del Usuario"
        # Dependiendo de la zona donde se hizo click se realiza una accion 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Borramos Mensaje para el Usuario
            self.userview.mensaje.update_prompt("")
            x, y = event.pos
            if self.userview.salir.collidepoint(x, y) or self.userview.apagar.collidepoint(x, y):
                # Click para Cerrar Sesion o Apagar Equipo
                band_access = self.salir_sistema()
                # Click en Cerrar Sesion
                if self.userview.salir.collidepoint(x, y):                
                    if band_access == False:
                        self.loginview.crear_interfaz()

                # Click en Boton Apagar
                if self.userview.apagar.collidepoint(x, y):
                    self.controlador.ApagarEquipo()
            if self.userview.asistencia.collidepoint(x, y):
                if self.user_controlador.get_user_type() == "alum" and self.modulo_asistencia == True:
                    self.asistview.crear_interfaz()
                    self.asistview.usuario_logeado.update_prompt(self.user_controlador.get_name_user())
                    self.clase_asistencia_alumno()
                    band_asist = True
        return band_access,band_asist
    
    def eventos_asistview(self,event,band_asist):
        "Metodo para Los Eventos en la Vista de Asistencia"
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Borramos Mensaje para el Usuario
            self.asistview.mensaje.update_prompt("")
            x, y = event.pos
            if self.asistview.asistencia.collidepoint(x, y):
                self.registrar_asistencia()
            if self.asistview.regresar.collidepoint(x, y):
                self.userview.crear_interfaz()
                self.userview.usuario_logeado.update_prompt(self.user_controlador.get_name_user())
                band_asist = False
            return band_asist
    
    
if __name__ == "__main__":
    interfaz = vista()
    interfaz.main()
    interfaz.iniciar()