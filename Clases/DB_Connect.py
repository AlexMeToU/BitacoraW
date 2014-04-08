# -*- coding: utf-8 *-*
'''
Created on 29/01/2014
@author: Admin
'''
import MySQLdb

class DB_Connect:

    def __init__(self, db_host='172.16.15.1',db_port=3306 , db_user='kabl', db_pass='Asist.3',
                 db_name='dbnovauniversitas'):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def conectar(self):
        """Crear una conexión con la base de datos"""
        self.db = MySQLdb.connect(host=self.db_host, port=self.db_port, user=self.db_user,
                              passwd=self.db_pass, db=self.db_name)


    def abrir_cursor(self):
        """Abrir un cursor"""
        self.cursor = self.db.cursor()

    def ejecutar_consulta(self, query, values=''):
        """Ejecutar una consulta"""
        if values != '':
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

    def traer_datos(self):
        """Traer todos los registros"""
        self.rows = self.cursor.fetchall()

    def send_commit(self, query):
        """Enviar commit a la base de datos"""
        sql = query.lower()
        es_lectura = sql.count('select')
        if es_lectura < 1:
            self.db.commit()

    def cerrar_cursor(self):
        """Cerrar cursor"""
        self.cursor.close()

    def ejecutar(self, query, values=''):
        """Compilar todos los procesos"""
        self.conectar()
        self.abrir_cursor()
        self.ejecutar_consulta(query, values)
        self.send_commit(query)        
        self.traer_datos()
        self.cerrar_cursor()
        return self.rows
