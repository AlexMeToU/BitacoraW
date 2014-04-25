# -*- coding: utf-8 *-*
#!/usr/bin/env python
'''
Created on 28/01/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import os
import sys
import subprocess
import threading
import time
#import logging
from datetime import datetime
# -----------
# Constantes
# -----------
apagarW = "shutdown /s /f /t 01"
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import model
import Clases.usuario
import Clases.filtro
import Clases.procesos
import Clases.windows
# ------------------------------
# Funcion principal del Programa
""" Controlador del Login"""
# ------------------------------


class controlador:
    
    def __init__(self):
        # Creamos un objeto usuario para la informacion del usuario a logear
        self.usuario = Clases.usuario.Usuario()
        
        # Creamos un objeto modelo para comunicarnos con el MODELO de la Aplicacion
        self.modelo = model.modelo()
        
        # Creamos un objeto proceso para controlar los Procesos del Equipo
        self.proceso = Clases.procesos.Procesos()
        
        # Creamos un objeto proceso para controlar los Elementos de Windows
        #self.win = Clases.windows.Windows()
        
        # Diccionario con los Tipos de Usuario del Sistema
        self.tipo_usuarios = {"profesor":"prof","asistente":"asist","alumno":"alum"}
        
        # Instancia a la Clase filtro
        self.filtro = Clases.filtro.filtro()
        
    """---------------------------------------Metodos-------------------------------------------------------"""
    def Obtener_Hora_Servidor(self):
        "Se Verifica la Hora del Servidor"
        consulta,edo_consulta = self.modelo.hora_sistema()
        if edo_consulta == "SUCCESS":
            self.usuario.hora_inicio = consulta[0][0]
        cad = str (self.usuario.hora_inicio)
        #logging.info('Hora del Sistema:')
        #logging.info(cad)
        return edo_consulta

    def registrar_inicio (self):
        "Se Registra el Inicio de Sesion"
        return self.modelo.registrar_inicio(self.usuario.clvUsu,self.usuario.hora_inicio,self.usuario.IP_Equipo)
        
    def obtener_usuario_logeado(self):
        return self.usuario

    """--------------------------------------Eventos-------------------------------------------------------"""

    def Iniciar_Sesion(self,usuario,pwd):
        "Click en Boton Iniciar Sesion"
        # Se obtienen los datos ingresados en el formulario de Logeo
        self.usuario.usuario = self.filtro.filtrar_cadena(usuario) 
        self.usuario.pwd = self.filtro.filtrar_cadena(pwd)
        consulta = ""
        # Se compara el usuario y pwd ingresado con los del Super Usuario
        if self.usuario.usuario == "super_usuario" and self.usuario.pwd =="COZDSOWLBOXY":
            #logging.info('Se logeo Super')
            #logging.info ("Hora de Inicio = ["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]")
            consulta = None
            #Recuperamos el Explorer y Matamos al Monitor_Controller
            self.Recuperar_Procesos()
            return "super"
        else:
            # Buscamos en Cada Tipo de Usuario los Datos Ingresados
            for key in self.tipo_usuarios.keys():
                if self.tipo_usuarios[key] == "alum":
                    # Primero se verifica que sea un Alumno
                    consulta,edo_consulta = self.modelo.validar_usuario_alumno(self.usuario.usuario,self.usuario.pwd)
                    # Si la Consulta Falla enviamos el Mensaje a la Vista
                    if edo_consulta == "FAILED_VALIDATE":
                        return edo_consulta
                    else:
                        if len(consulta) > 0:
                            for registro in consulta:
                                # Guardamos la informacion recibida desde la BD
                                self.usuario.tipo_usuario = self.tipo_usuarios[key]
                                self.usuario.nombre = registro [1] #Nombre
                                self.usuario.apePat = registro [2] #ApePat
                                self.usuario.apeMat = registro [3] #ApeMat
                                self.usuario.clvUsu = registro [0] #Matricula
                                self.usuario.nombre_usuario = registro[1]+' '+registro[2]+' '+registro[3]
                            break
                            
                elif self.tipo_usuarios[key] == "asist":
                    # Se verifica que sea un Asistente
                    consulta,edo_consulta = self.modelo.validar_usuario_tecaux(self.usuario.usuario,self.usuario.pwd)
                    # Si la Consulta Falla enviamos el Mensaje a la Vista
                    if edo_consulta == "FAILED_VALIDATE":
                        return edo_consulta
                    else:
                        if len(consulta) > 0:
                            for registro in consulta:
                                # Guardamos la informacion recibida desde la BD
                                self.usuario.tipo_usuario = self.tipo_usuarios[key]                          
                                self.usuario.nombre = registro [1] #Nombre
                                self.usuario.apePat = registro [2] #ApePat
                                self.usuario.apeMat = registro [3] #ApeMat
                                self.usuario.graAca = registro [4] #Grado
                                self.usuario.clvUsu = registro [5] #log
                                self.usuario.nombre_usuario = registro[4]+' '+registro[1]+' '+registro[2]+' '+registro[3]
                            break
                elif self.tipo_usuarios[key] == "prof":
                    # Se verifica que sea un Profesor 
                    consulta,edo_consulta = self.modelo.validar_usuario_profesor(self.usuario.usuario,self.usuario.pwd)
                    # Si la Consulta Falla enviamos el Mensaje a la Vista                    
                    if edo_consulta == "FAILED_VALIDATE":
                        return edo_consulta
                    else:
                        if len(consulta) > 0:
                            for registro in consulta:
                                # Guardamos la informacion recibida desde la BD
                                self.usuario.tipo_usuario = self.tipo_usuarios[key]
                                self.usuario.nombre = registro [1] #Nombre
                                self.usuario.apePat = registro [2] #ApePat
                                self.usuario.apeMat = registro [3] #ApeMat
                                self.usuario.graAca = registro [4] #Grado
                                self.usuario.clvUsu = registro [5] #log
                                self.usuario.nombre_usuario = registro[4]+' '+registro[1]+' '+registro[2]+' '+registro[3]
                            break

            if len(consulta) > 0:
                self.usuario.Obtener_IP_Equipo()
                if self.usuario.IP_Equipo == "0.0.0.0":
                    #print "Fallo al Leer IP"
                    return "FAILED_GET_IP"
                
                edo_hora_servidor = self.Obtener_Hora_Servidor()
                if edo_hora_servidor == "FAILED_GET_HOUR":
                    #print "Fallo al Leer Hora del Servidor"
                    return edo_hora_servidor
                edo_registro = self.modelo.registrar_inicio(self.usuario.clvUsu,self.usuario.hora_inicio,self.usuario.IP_Equipo)
                if edo_registro == "SUCCESS_QUERY_REGISTER":
                    # Si el Registro de Sesion fue SUCCESS
                    self.Recuperar_Procesos()
                return edo_registro
            else:
                #print "Usuario No Valido"
                return "USER_NO_VALIDO"

    def Habilitar_elementos_windows(self):
        "Metodo para Mostrar Barra Menu y Boton Inicio"
        #self.win.Show_taskbar()
        #self.win.Show_starbutton()
        #self.win.Enable_Shorcut()
                
    def Deshabilitar_elementos_windows(self):
        "Metodo para Ocultar Barra Menu y Boton Inicio"
        #self.win.Hide_taskbar()
        #self.win.Hide_starbutton()
        #self.win.Disenable_Shorcut()
        
    def ApagarEquipo(self):
        "Click en Boton Apagar Equipo"
        os.system(apagarW)
            
    """-----------------------------------------PROCESOS DE WIN---------------------------------------------"""
    def Iniciar_Procesos(self):
        "Se Inicia el Proceso Monitor_Controller"
        # Se busca que no este corriendo actualmente el Proceso Monitor Controller
        resultado = self.proceso.Buscar_Proceso("monitor_controller.exe")
        if resultado == 0:
            # Creamos un Hilo para el Proceso Monitor Controller
            #logging.info('Se inicia Proceso Monitor Controller')
            self.t_monitor = threading.Thread(target=self.daemon_monitor, name='monitor_controller')
            self.t_monitor.setDaemon(True)
            self.t_monitor.start()
        
    def Recuperar_Procesos(self):
        "Se Inicia el Proceso Explorer y Finaliza Proceso Monitor_Controller"
        # Se finaliza el Proceso Monitor_Controller
        #logging.info('Se Finaliza Proceso Monitor Controller')
        self.proceso.Finalizar_Proceso("monitor_controller.exe")
            
        # Se busca que no este corriendo actualmente el Proceso Explorer, Si esta algun Alguno lo Eliminamos
        #resultado = self.proceso.Buscar_Proceso("explorer.exe")
        #while resultado == 1:
            #self.proceso.Finalizar_Proceso("explorer.exe")
            #resultado = self.proceso.Buscar_Proceso("explorer.exe")
        #if resultado == 0:
            # Creamos un Hilo para el Proceso Explorer
            #logging.info('Se inicia Proceso Explorer')
            #self.t_explorer = threading.Thread(target=self.daemon_explorer, name='explorer')
            #self.t_explorer.setDaemon(True)
            #self.t_explorer.start()
    """-----------------------------------------Hilos-------------------------------------------------------"""
    
    def daemon_monitor(self):
        """Hilo para Ejecutar Proceso Monitor_Controller"""
        #subprocess.call(['C:/python27/dist/Monitor/dist/monitor_controller.exe'])
        #subprocess.call(['../../Ejecutables/Monitor/dist/monitor_controller.exe'])
        subprocess.call(['C:/Program Files/Bitacora/Ejecutables/Monitor/dist/monitor_controller.exe'])
        time.sleep(2)

    def daemon_explorer(self):
        """Hilo para Ejecutar Proceso Explorer"""
        subprocess.call(['C:/Windows/explorer.exe'])
        time.sleep(2)            