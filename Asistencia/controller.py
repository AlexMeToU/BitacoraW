# -*- coding: utf-8 *-*
'''
Created on 05/02/2014

@author: Admin
'''
# -----------
# Librerias
# -----------
import time
import datetime
# -----------
# Constantes
# -----------
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
import model
# ------------------------------
# Funcion principal del Programa
""" Controlador de Asistencia del Usuario"""
# ------------------------------


class controlador:
    def __init__(self):
        # Instancia para el Modelo
        self.modelo = model.modelo()        

    """---------------------------------------Metodos-------------------------------------------------------"""
    def set_usuario(self,user):
        "Metodo para Instancia para los Datos del Usuario Logeado"
        self.usuario = user

    def get_user_type(self):
        "Metodo que nos da el Tipo de Usuario Logeado"
        return self.usuario.obtener_tipo_usuario()

    def reset_asist_values(self):
        "Reseteamos las Variables para La Interfaz de Asistencia"
        self.band_clase = False
        self.asistencia_alumno = False
        self.usuario.clvHor = ""
        self.usuario.materia = ""
    
    def Obtener_Hora_Fecha_Servidor(self):
        "Se Verifica la Fecha del Servidor"
        fecha_consulta = ""
        dia = ""
        hora = ""
        edo_consulta = ""
        consulta,edo_consulta = self.modelo.hora_sistema()
        if edo_consulta == "SUCCESS":
            # Obtenemos la Fecha se solicito Boton de Registrar Asistencia
            fecha = datetime.datetime.strptime(str (consulta[0][0]),"%Y-%m-%d %H:%M:%S")
            tmp = str (consulta[0][0])
            fecha_consulta = str (tmp[:tmp.find(' ')] )
            hora_consulta = str (tmp[tmp.find(' ')+1:] )

            # Guardamos el Dia y la Hora
            # 0 es Domingo 6 es Sabado

            dia = int(fecha.strftime('%w'))
            # 24 Hrs  00 - 23
            hora = int(fecha.strftime('%H'))
            # 0 - 60 Min
            minuto = int(fecha.strftime('%M'))
            print "DIA: ",dia," Hora: ",hora
            print fecha_consulta
        return (fecha_consulta,hora_consulta,dia,hora,minuto),edo_consulta
    
    def obtener_clvhor_clvmat(self,fecha_consulta,dia,hora):
        "Obtenemos la Clave del Horario y la Clave de la Materia"
        consulta = ""
        edo_consulta = ""

        # Buscamos La clave de la Materia en el Horario
        consulta,edo_consulta = self.modelo.clase_horario(self.usuario.gpo,dia,hora)        
        if edo_consulta == "SUCCESS":
            if consulta:
                # La entrada esta marcada en el Horario
                return consulta,edo_consulta
            else:
                # Verificar si es Clase Normal=8 o Laboral Permutable=6
                consulta2,edo_consulta2 = self.modelo.fecha_calendario(fecha_consulta)
                if edo_consulta2 == "SUCCESS":
                    if consulta2:
                        staCalEsc = consulta2[0][0]
                        staCalEsc2 = consulta2[0][1]
                        print "Sta1 = ",staCalEsc," Sta2 = ",staCalEsc2
                        if staCalEsc == 6 or staCalEsc == 8 or staCalEsc2 == 6 or staCalEsc2 == 8:
                            dia = 1
                            consulta,edo_consulta = self.modelo.clase_horario(self.usuario.gpo,dia,hora)        
                        else:
                            consulta = consulta2
                            edo_consulta = edo_consulta2
                    else:
                        consulta = consulta2
                        edo_consulta = edo_consulta2
                else:
                    consulta = consulta2
                    edo_consulta = edo_consulta2
        return consulta,edo_consulta 
    
    def obtener_clase_alumno(self,fecha_consulta,dia,hora):
        "Obtener la Clase del Alumno"
        clase = ""
        mensaje = ""
        consulta,edo_consulta = self.modelo.gpo_alum(self.usuario.clvUsu)
        if edo_consulta == "SUCCESS":
            if consulta:
                for gpo in consulta:
                    print "Gpo: ",gpo[0] # Grupo del Alumno
                    self.usuario.gpo = gpo[0]
                    # Buscamos La clave de la Materia en el Horario
                    consulta2,edo_consulta2 = self.obtener_clvhor_clvmat(fecha_consulta,dia,hora)
                    #consulta2,edo_consulta2 = self.modelo.clase_horario(self.usuario.gpo,dia,hora)
                    if edo_consulta2 == "SUCCESS":
                        if consulta2:
                            print "clvHorNov: ",consulta2[0][0] 
                            print "clvMatNov: ",consulta2[0][1] 
                            self.usuario.clvHor = consulta2[0][0] # Clave del Horario
                            self.usuario.materia = consulta2[0][1] # Clave de la Materia
                            self.band_clase = True # Si hay Clase a esta Hora
                            
                            # BUscamos el Nombre de la Materia
                            consulta3,edo_consulta3 = self.modelo.nombre_materia(consulta2[0][1])
                            if edo_consulta3 == "SUCCESS":
                                if consulta3:
                                    print consulta3[0][0]                                    
                                    clase = str (consulta3[0][0]) # Nombre de la Materia
                                else:
                                    clase = str (consulta2[0][1]) # Clave de la Materia (La Clave no esta relacionada con algun Nombre)
                                mensaje = ""
                                return clase,mensaje
                            else:
                                print "Fallo Consulta a Nombre de Materia"
                                clase = ""
                                mensaje = edo_consulta
                                return clase,mensaje
                        else:
                            clase = "NO HAY CLASE A ESTA HORA"
                            mensaje = ""
                            self.band_clase = False # No hay Clase a esta Hora
                            return clase,mensaje
                    else:
                        print "Fallo Consulta a Clase del Horario"
                        clase = ""
                        mensaje = edo_consulta
                        return clase,mensaje
            else:
                clase = "SIN GRUPO"
                mensaje = "EL ALUMNO NO TIENE UN GRUPO ASIGNADO"
                return clase,mensaje
        else:
            print "Fallo Consulta a Grupo del Alumno"
            clase = ""
            mensaje = edo_consulta
            return clase,mensaje
    
    def obtener_asist_alum(self,fecha_consulta):
        "Se Obtiene la Asistencia del Alumno para esa Clase"
        mensaje = ""
        asistencia = ""
        consulta,edo_consulta2 =self.modelo.buscar_asist_alum(self.usuario.clvHor,fecha_consulta,self.usuario.clvUsu)
        if edo_consulta2 == "SUCCESS":
            if consulta:
                print consulta
                asistencia = "("+ str (consulta[0][5]) + ") " + str (consulta[0][4])
                self.asistencia_alumno = True
            else:
                asistencia = "Sin Asistencia"
                self.asistencia_alumno = False
        else:
            asistencia = "No se Puede Determinar"
        mensaje = edo_consulta2
        return asistencia,mensaje
    
    """--------------------------------------Eventos-------------------------------------------------------"""
    def registrar_asistencia(self,fecha_consulta,hora_consulta,dia,hora,minuto):
        "Se Registra Asistencia del Alumno"
        # Si es True el alumno ya tiene Asistencia para esta Materia en este dia
        asistencia = ""
        edo_insercion = ""
        if hora == 9 or hora == 16:
            print "Tolerancia de 10"
            if minuto >= 0 and minuto <=10:
                print "A"
                status = "A"
            else:
                print "R"
                status = "R"
        else:
            print "Tolerancia de 5"                
            if minuto >= 0 and minuto <=5:
                print "A"
                status = "A"
            else:
                print "R"
                status = "R"
        
        if self.asistencia_alumno == True:
            print "EL alumno ya Tiene Asistencia para la Materia"
            asistencia = ""                
            edo_insercion = "SIN_INSERCION"
            return asistencia,edo_insercion                
        else:
            # Consultar si el Equipo ya fue usado para Registrar la Asistencia de un Alumno
            consulta,edo_consulta = self.modelo.buscar_ip_asist(self.usuario.clvHor,fecha_consulta,self.usuario.IP_Equipo)
            if edo_consulta == "SUCCESS":
                if consulta:
                    print "La IP ya esta ocupada.Favor de registrarse en otra maquina"
                    asistencia = "Sin Asistencia"
                    edo_insercion = "La IP ya esta ocupada.Favor de registrarse en otra maquina"
                    return asistencia,edo_insercion                        
                else:
                    # Hay Clase para registrar la Asistencia
                    if self.band_clase == True:
                        edo_consulta = self.modelo.registrar_asistencia(self.usuario.clvUsu,self.usuario.clvHor,fecha_consulta,hora_consulta,status,self.usuario.IP_Equipo)
                        if edo_consulta == "SUCCESS_QUERY_ATTENDANCE":
                            print "Insercion hecha"
                            consulta2,edo_consulta2 = self.obtener_asist_alum(fecha_consulta)
                            if edo_consulta2 == "SUCCESS":
                                asistencia = consulta2
                                print asistencia
                            else:
                                asistencia = "Error al Obtener la Asistencia"
                            edo_insercion = edo_consulta2
                            return asistencia,edo_insercion
                        else:
                            print "Error en Insercion"
                        asistencia = ""
                        edo_insercion = edo_consulta
                        return asistencia,edo_insercion
            else:
                print "No se Puede Consultar la IP en la Tabla de Asistencia"
                asistencia = ""                
                edo_insercion = edo_consulta
                return asistencia,edo_insercion
        return asistencia,edo_insercion