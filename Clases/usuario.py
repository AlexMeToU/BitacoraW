# -*- coding: utf-8 *-*
'''
Created on 14/02/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import socket
#import logging
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------

class Usuario():
    
    def __init__(self):
        "Los atributos del Usuario"
        self.graAca = ''
        self.usuario = ''
        self.pwd = ''
        self.nombre_usuario = ''
        self.nombre = ''
        self.apePat= ''
        self.apeMat= ''
        self.clvUsu= ''
        self.hora_inicio = ''
        self.hora_salida = ''
        self.IP_Equipo='0.0.0.0'

    def Obtener_IP_Equipo (self):
        "Se Obtiene la IP del Equipo"
        self.ip_gethostname()

    def ip_gethostname(self):
        "Se Obtiene la IP del Equipo por medio del hostname"
        ip = socket.gethostbyname_ex(socket.gethostname())[2]
        self.IP_Equipo = ip[0][:15]
        cad = str (self.IP_Equipo)
        #logging.info("IP:")
        #logging.info(cad)

    def obtener_usuario(self):
        return self.nombre_usuario
    
    def reset_usuario(self):
        "Metodo que resetea los Atributos del Usuario"
        self.graAca = ''
        self.usuario = ''
        self.pwd = ''
        self.nombre_usuario = ''
        self.nombre = ''
        self.apePat= ''
        self.apeMat= ''
        self.clvUsu= ''
        self.hora_inicio = ''
        self.hora_salida = ''
        self.IP_Equipo='0.0.0.0'