from app_encuesta_dojo.config.mysqlconnection import connectToMySQL
from flask import flash

class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.ubicacion=data['ubicacion']
        self.idioma=data['idioma']
        self.comentario=data['comentario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save_dojo(cls,data):
        query="INSERT INTO dojos(nombre,ubicacion,idioma,comentario) VALUES(%(nombre)s,%(ubicacion)s,%(idioma)s,%(comentario)s);"
        return connectToMySQL('esquema_encuesta_dojo').query_db(query,data)

    @classmethod
    def last_id(cls):
        query="SELECT * FROM dojos order by id desc limit 1;"
        return connectToMySQL('esquema_encuesta_dojo').query_db(query)

    @classmethod
    def get_all_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('esquema_encuesta_dojo').query_db(query)
        dojos = []
        for djo in results:
            dojos.append( cls(djo) )
        return dojos

    @classmethod
    def get_one_dojo(cls,data):
        query = "SELECT * FROM dojos WHERE id=%(id)s;"
        results = connectToMySQL('esquema_encuesta_dojo').query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validar_dojo(registro):
        is_valid = True # asumimos que esto es true
        if len(registro['nombre'])==0:
            flash("Nombre no debe estar vacio")
            is_valid = False
        elif len(registro['nombre']) < 2:
            flash("Nombre debe contener al menos 2 caracteres")
            is_valid = False
        if registro['ubicacion'] == "":
            flash("Debe seleccionar una ubicacion")
            is_valid = False
        if registro['idioma'] == "":
            flash("Debe seleccionar un idioma")
            is_valid = False
        if len(registro['comentario'])==0:
            flash("Comentario no debe estar vacio")
            is_valid = False
        elif len(registro['comentario']) < 2:
            flash("Comentario debe contener al menos 2 caracteres")
            is_valid = False
        return is_valid