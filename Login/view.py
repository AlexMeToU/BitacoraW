# -*- coding: utf-8 *-*
#!/usr/bin/ python
'''
Created on 19/03/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
from ctypes import windll
#import logging
from datetime import datetime
import pygame
from pygame.locals import *
import sys
sys.path.append("..")
# -----------
# Constantes
# -----------
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

S_WIDTH = 480
S_HEIGHT = 150

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import Clases.eztext
import controller
import InterfazUsuario.controller
# ------------------------------
# Funcion principal de la Aplicacion
# ------------------------------
"Vista de La Aplicacion para llevar un control de los Alumnos y los Equipos en las Aulas"
 
class vista():
     
    def main(self):
        "Metodo Main Principal"
        #logging.basicConfig(filename='view.log',level=logging.DEBUG)
        #self.cabecera()
        # Cargamos todo lo relacionado a pygame
        pygame.init()
        
        # Set up a variable that calls the "SetWindowPos" in user32
        self.SetWindowPos = windll.user32.SetWindowPos
        
        # Creamos las Instancias a los Controladores
        self.controlador = controller.controlador()
        self.user_controlador = InterfazUsuario.controller.controlador()
        
        # Creamos la Ventana Login
        self.dimencionar_ventana(SCREEN_WIDTH, SCREEN_HEIGHT,"pygame.FULLSCREEN", "Login")
        
        # Cargamos Las imagenes a Usar
        self.cargar_imagenes()

        # Cargamos los TextBox de la Aplicacion
        self.cargar_textbox()
        
        # Indicamos la posicion de las "Surface" sobre la ventana Login
        self.surface_login()
        
        # Definimos las areas de los surfaces de los botones
        self.cargar_botones()

        # create the pygame clock
        self.clock = pygame.time.Clock()

    def cabecera(self):
        "Metodo para La Cabecera del Script"
        print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'
        print '        Se inicia Script           '
        print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'
        #logging.info('\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n        Se inicia Script           \n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
        #Guardamos la Hora de Ejecucion del script
        #logging.info ("Hora de Inicio = ["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]")


    def iniciar(self):
        "Metodo para El bucle Principal de la Aplicacion"
        # Si el SO es win Matamos al Explorer y Ejecutamos el Proceso Monitor_Controller
        self.controlador.Iniciar_Procesos()
        
        # Bandera para permitir escritura en los TextBox
        band_write = 1
        # Bandera para el acceso al equipo
        band_access = False
        # se muestran lo cambios en pantalla
        # el bucle principal del juego

        while True:
            # Nos Aseguramos que el codigo corre a 30 fps
            self.clock.tick(30)
            
            # Empezamos a capturar la lista de Eventos
            events = pygame.event.get()
            
            # Posibles entradas del teclado y mouse
            for event in events:
                if event.type == pygame.QUIT:
                    # Intentaron cerrar la ventana
                    "Click en Boton Cerrar"
                    #sys.exit()
                elif event.type == KEYUP:
                    # Para Identificar cuando la tecla Caps se Desactivo
                    if event.key == pygame.K_CAPSLOCK:
                        self.usuario.Mayus = False
                        self.pwd.Mayus = False                    
                elif event.type == KEYDOWN:
                    # Para Identificar cuando la tecla Caps se Activo
                    if event.key == pygame.K_CAPSLOCK:
                            self.usuario.Mayus = True
                            self.pwd.Mayus = True                    
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
                    self.mensaje.update_prompt("")
                    self.mensaje_to_user.update_prompt("")
                    
                    # Dependiendo de la zona donde se hizo click se realiza una accion 
                    x, y = event.pos
                    # Si la Bandera == False se checan las surfaces del Login
                    if band_access == False:
                        if x>= 505 and x <= 755 and y >= 360 and y<= 385:
                            "Click en Textbox usuario"
                            band_write = 1
                        elif x>= 505 and x <= 755 and y >= 410 and y<= 440:
                            "Click en Textbox pwd"
                            band_write = 2
                        elif self.entrar.collidepoint(x, y):
                            "Click en Boton Entrar"
                            band_access = self.ingresar_sistema()
                        elif self.apagar.collidepoint(x, y):
                            "Click en Boton Apagar"
                            # Registramos La Hora en Que se Apago el Equipo                            
                            #logging.info ("Se Apaga Equipo: ["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]")
                            self.controlador.ApagarEquipo()
                            band_write = 0
                        else:
                            band_write = 0
                    elif band_access == True:
                        # Ventana de Usuario
                        if self.salir.collidepoint(x, y) or self.apagar.collidepoint(x, y):
                            # Click para Cerrar Sesion o Apagar Equipo
                            "Click en Boton Salir"
                            res = self.user_controlador.registrar_Salida()
                            if res == "SUCCESS_QUERY_REGISTER":
                                #logging.info('Se Cerro la Sesion')
                                if self.apagar.collidepoint(x, y): 
                                    "Click en Boton Apagar"
                                    # Registramos La Hora en Que se Apago el Equipo           
                                    #logging.info ("Se Apaga Equipo: ["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]")                                                  
                                    self.controlador.ApagarEquipo()
                                else:    
                                    # Redimencionamos la Ventana a FullScreen y sus surfaces
                                    self.dimencionar_ventana(SCREEN_WIDTH, SCREEN_HEIGHT,"pygame.FULLSCREEN", "Login")
                                    self.apagar = self.bapagar.get_rect(center=(797, 501))
                                    # Reseteamos los TextBox del Login
                                    self.usuario.reset_input()
                                    self.pwd.reset_input()
                                    self.user_controlador.reset_usuario()
                                    self.controlador.Iniciar_Procesos()
                                    band_write = 1
                                    band_access = False
                            elif res == "FAILED_GET_HOUR":
                                # Fallo Al Obtener la Hora del Servidor
                                "Fallo en Realizar Registro de Fin de Sesion"
                                band_access = True
                                band_write = 0
                                self.mensaje_to_user.update_prompt("Hora No Valida")  
                            elif res == "FAILED_QUERY_REGISTER":
                                # Fallo en Realizar Registro de Fin de Sesion
                                "Fallo en Realizar Registro de Fin de Sesion"
                                band_access = True
                                band_write = 0
                                self.mensaje_to_user.update_prompt("No se Realizo el Fin de Sesion")
                                
            if band_write == 1:
                # Se ingresan datos en el TextBox del Usuario
                self.usuario.update(events)
            elif band_write == 2:
                # Se ingresan datos en el TextBox del Pwd
                self.pwd.update(events)

            if band_access == True:
                #Obtenemos el Nombre del Usuario Logeado para mostrarlo en la Ventana Usuario
                self.usuario_logeado.update_prompt(self.user_controlador.get_name_user())
                # Se muestran los Surfaces de la Ventana Usuario
                self.surface_user()
                self.usuario_logeado.draw(self.screen)
                self.mensaje_to_user.draw(self.screen)
                
            elif band_access == False:
                # Se muestran los Surfaces de la Ventana Login
                self.surface_login()
                self.usuario.draw(self.screen)
                self.pwd.draw_pwd(self.screen)
                self.mensaje.draw(self.screen)
            
            # refresh the display
            pygame.display.flip()
 
    def ingresar_sistema(self):
        # Se valida el Usuario ingresado
        res = self.controlador.Iniciar_Sesion(self.usuario.getTxt(), self.pwd.getTxt())
        # Si el usuario es el Admin se cierra la Aplicacion
        if res == "super":
            "Usuario Super"
            sys.exit(0)
        elif res == "SUCCESS_QUERY_REGISTER":
            # Si el Usuario es valido y se realizo el registro de sesion se cambia la Interfaz a la de Usuario
            "Usuario Valido"
            #logging.info('Se Inicio Sesion')            
            band_access = True
            # Redimencionamos la ventana y sus Surface
            self.dimencionar_ventana(S_WIDTH, S_HEIGHT,"pygame.RESIZABLE", "Usuario")
            self.apagar = self.bapagar.get_rect(center=(434, 103))
            # Pasamos la Informacion del usuario Logeado al Controlador del Usuario
            self.user_controlador.set_usuario(self.controlador.obtener_usuario_logeado())
            return band_access
        elif res == "USER_NO_VALIDO":
            # Si el Usuario no es valido se manda mensaje a la Ventana
            "Usuario no valido"
            band_access = False
            self.mensaje.update_prompt("Usuario o Pwd no valido")
            return band_access
        elif res == "FAILED_VALIDATE":
            # Fallo Al realizar la Consulta
            "Fallo en Realizar Consulta"
            band_access = False
            self.mensaje.update_prompt("No se puede Consultar el Usuario")
            return band_access
        elif res == "FAILED_GET_IP":
            # Fallo Al Obtener la IP del Equipo
            "Fallo Al Obtener la IP del Equipo"
            band_access = False
            self.mensaje.update_prompt("IP No Valida")
            return band_access
        elif res == "FAILED_GET_HOUR":
            # Fallo Al Obtener la Hora del Servidor
            "Fallo Al Obtener la IP del Equipo"
            band_access = False
            self.mensaje.update_prompt("Hora No Valida")
            return band_access
        elif res == "FAILED_QUERY_REGISTER":
            # Fallo en Realizar Registro de Inicio de Sesion
            "Fallo en Realizar Registro de Inicio de Sesion"
            band_access = False
            self.mensaje.update_prompt("No se Realizo el Inicio de Sesion")
            return band_access
 
    def cargar_imagenes(self):
        "Metodo para Cargar las Imagenes a la Aplicacion"
        # Cargammos Las Imagenes desde Archivo
        imagenfondo = "C:/Program Files/Bitacora/src/images/Fondo.png"
        #imagenform = "../../src/images/Fondo_Panel1.png"
        imagenform = "C:/Program Files/Bitacora/src/images/Fondo_Panel.png"
        imagenuser_interface = "C:/Program Files/Bitacora/src/images/user_interface.png"
        imagenbEntrar = "C:/Program Files/Bitacora/src/images/Entrar.png"
        imagenbCerrar = "C:/Program Files/Bitacora/src/images/Cerrar.png"
        imagenbApagar = "C:/Program Files/Bitacora/src/images/Apagar.png"

        # Cargamos el fondo y las imagenes para la Ventana Login
        self.fondo = pygame.image.load(imagenfondo).convert()
        self.form = pygame.image.load(imagenform).convert_alpha()
        self.bentrar = pygame.image.load(imagenbEntrar).convert_alpha()
        self.bapagar = pygame.image.load(imagenbApagar).convert_alpha()

        # Cargamos el fondo y las imagenes para la Ventana Usuario
        self.user_interface = pygame.image.load(imagenuser_interface).convert()
        self.bsalir = pygame.image.load(imagenbCerrar).convert_alpha()       
 
    def cargar_textbox(self):
        "Metodo para cargar TextBox y Textos a la Aplicacion"
        # Se carga el Tipo de Fuente
        #self.fuente = pygame.font.SysFont("MS Reference Sans Serif", 12, bold=True, italic=False)
        self.fuente = pygame.font.SysFont("Arial", 12, bold=True, italic=False)
        
        # Cargamos los TextBox
        self.usuario = Clases.eztext.Input(x=570, y=365, font = self.fuente, maxlength=20, color=(159,161,164), prompt='')
        self.pwd = Clases.eztext.Input(x=570, y=415, font = self.fuente, maxlength=20, color=(159,161,164), prompt='')
        
        # Cargamos los Mensajes
        self.mensaje = Clases.eztext.Input(x=520, y=335, font = self.fuente, maxlength=20, color=(255,0,0), prompt='')
        self.usuario_logeado = Clases.eztext.Input(x=25, y=45, font = self.fuente, maxlength=20, color=(109,110,113), prompt='')
        self.mensaje_to_user = Clases.eztext.Input(x=95, y=90, font = self.fuente, maxlength=50, color=(255,0,0), prompt='')
        
    def cargar_botones(self):
        "Metodo para cargar Botones a la Aplicacion"
        self.entrar = self.bentrar.get_rect(center=(543, 484))
        self.apagar = self.bapagar.get_rect(center=(797, 501))
        self.salir = self.bsalir.get_rect(center=(45, 103))
        
    def dimencionar_ventana(self,width, heigth,flag,titulo):
        "Metodo Para Dimencionar la Ventana"
        if flag == "pygame.FULLSCREEN":
            # Modo Sin Bordes para el Login
            self.screen = pygame.display.set_mode((width, heigth), pygame.NOFRAME)
            # Supply the hWnd(Window Handle) with the window ID returned from a call to display.get_wm_info()
            # This sets the window to be on top of other windows.
            self.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)
        else:
            # Modo Resizable para Usuario
            self.screen = pygame.display.set_mode((width, heigth), pygame.RESIZABLE)
        pygame.display.set_caption(titulo)
        
    def surface_login(self):
        "Metodo para Agregar los Surface a la Ventana Login"
        self.screen.blit(self.fondo, (0,0))
        self.screen.blit(self.form, (420,300))
        self.screen.blit(self.bentrar, self.bentrar.get_rect(center=(543, 484)))
        self.screen.blit(self.bapagar, self.bapagar.get_rect(center=(797, 501)))

    def surface_user(self):
        "Metodo para Agregar los Surface a la Ventana Usuario"
        self.screen.blit(self.user_interface, (0,0))
        self.screen.blit(self.bsalir, self.bsalir.get_rect(center=(45, 103)))
        self.screen.blit(self.bapagar, self.bapagar.get_rect(center=(434, 103)))



if __name__ == "__main__":
    interfaz = vista()
    interfaz.main()
    interfaz.iniciar()