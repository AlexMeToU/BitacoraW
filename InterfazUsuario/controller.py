# -*- coding: utf-8 *-*
'''
Created on 05/02/2014

@author: Admin
'''
import model

class controlador:
    def __init__(self):
        # Instancia para el Modelo
        self.modelo = model.modelo()        

    """---------------------------------------Metodos-------------------------------------------------------"""
    def set_usuario(self,user):
        "Metodo para Instancia para los Datos del Usuario Logeado"
        self.usuario = user
    
    def get_name_user(self):
        "Metodo que nos da el Nombre Completo del Usuario Logeado"
        return self.usuario.obtener_usuario()

    def reset_usuario(self):
        self.usuario.reset_usuario()
        
    def imprimir_datos_usuario(self):
        self.usuario.Imprimir_valores()

    def Obtener_Hora_Servidor(self):
        "Se Verifica la Hora del Servidor"
        consulta,edo_consulta = self.modelo.hora_sistema()
        if edo_consulta == "SUCCESS":
            self.usuario.hora_salida = consulta[0][0]
        return edo_consulta
    """--------------------------------------Eventos-------------------------------------------------------"""
    def registrar_Salida(self):
        "Se Registra el Fin de Sesion"
        edo_hora_servidor = self.Obtener_Hora_Servidor()
        if edo_hora_servidor == "FAILED_GET_HOUR":
            return edo_hora_servidor
        return self.modelo.registrar_salida(self.usuario.clvUsu,self.usuario.hora_inicio,self.usuario.hora_salida,self.usuario.IP_Equipo)
