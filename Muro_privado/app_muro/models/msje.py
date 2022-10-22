from datetime import datetime
import math
from app_muro.models import user
from app_muro.config.mysqlconnection import connectToMySQL
from flask import flash

class Msje:
    def __init__( self , data ):
        self.idmsje = data['idmsje']
        self.mensaje = data['mensaje']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.remitente = data['remitente']
        self.destinatario = data['destinatario']
        self.nombre = data['nombre']
        self.on_users=[]
        self.allusers=[]
        self.on_msjes=[]

    def tiempo(self):
        now=datetime.now()
        dif=now - self.created_at
        if dif.days > 0:
            return f"{dif.days} dias atras"
        elif (math.floor(dif.total_seconds()/60))>=60:
            return f"{math.floor(dif.total_seconds()/60)/60} horas atras"
        elif dif.total_seconds()>=60:
            return f"{math.floor(dif.total_seconds()/60)} minutos atras"
        else:
            return f"{math.floor(dif.total_seconds())} segundos atras"

    @classmethod
    def save_msje(cls,data):
        query="INSERT INTO msjes(mensaje,remitente,destinatario) VALUES(%(mensaje)s,%(remitente)s,%(destinatario)s);"
        return connectToMySQL('muro_db').query_db(query,data)

    @classmethod
    def destroy_msje(cls,data):
        query = "DELETE FROM msjes WHERE idmsje = %(idmsje)s;"
        return connectToMySQL('muro_db').query_db(query,data)

    @classmethod
    def get_count_msjes(cls,data):
        query="SELECT count(*) as cont FROM msjes WHERE remitente=%(remitente)s;"
        return connectToMySQL('muro_db').query_db(query,data)

    @classmethod
    def get_msjes_one_user(cls,data):
        query = "SELECT * FROM msjes as m JOIN users as u ON m.remitente = u.iduser WHERE m.destinatario=%(destinatario)s order by u.nombre asc;"
        results = connectToMySQL('muro_db').query_db(query,data)
        lista_one_msje=[]
        for row_from_db in results:
            obj_onemsje=cls(row_from_db)
            obj_onemsje.allusers.append(user.User(row_from_db))
            lista_one_msje.append(obj_onemsje)
        return lista_one_msje

    @staticmethod
    def validar_msje(registro):
        is_valid = True # asumimos que esto es true
        if len(registro['mensaje']) < 5:
            flash("El mensaje debe contener al menos 5 caracteres")
            is_valid = False
        return is_valid