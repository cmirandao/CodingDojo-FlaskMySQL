from app_libros.config.mysqlconnection import connectToMySQL
from app_libros.models import libro

class Autor:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.on_libros=[]
    
    @classmethod
    def guardar_autor(cls,data):
        query="INSERT INTO autores(nombre) VALUES(%(nombre)s);"
        return connectToMySQL('esquema_libros').query_db(query,data)

    @classmethod
    def guardar_favorito(cls,data):
        query="INSERT INTO favoritos(autor_id,libro_id) VALUES(%(autor_id)s,%(libro_id)s);"
        return connectToMySQL('esquema_libros').query_db(query,data)

    @classmethod
    def ver_no_favoritos(cls,data):
        query="select * from autores where autores.id not in (select autor_id from favoritos where libro_id=%(id)s);"
        results=connectToMySQL('esquema_libros').query_db(query,data)
        autor_no_fav=[]
        for aufav in results:
            autor_no_fav.append(cls(aufav))
        return autor_no_fav

    @classmethod
    def get_all_autor(cls):
        query = "SELECT * FROM autores;"
        results = connectToMySQL('esquema_libros').query_db(query)
        autores = []
        for autr in results:
            autores.append( cls(autr) )
        return autores

    @classmethod
    def get_un_autor(cls,data):
        query = "SELECT * FROM autores WHERE id=%(id)s;"
        resultados = connectToMySQL('esquema_libros').query_db(query,data)
        return cls(resultados[0])

    @classmethod
    def destroy_autor(cls,data):
        query = "DELETE FROM autores WHERE id = %(id)s;"
        return connectToMySQL('esquema_libros').query_db(query,data)

# clase para hacer el join de las 2 tablas
    @classmethod
    def get_libros_autores(cls, data):
        query = """SELECT * FROM autores LEFT JOIN favoritos ON favoritos.autor_id = autores.id 
        LEFT JOIN libros ON favoritos.libro_id = libros.id WHERE autores.id = %(id)s"""
        results = connectToMySQL('esquema_libros').query_db(query,data)
        autor= []
        for row_from_db in results:
            libro_data = {
                "id" : row_from_db["libros.id"],
                "nombre" : row_from_db["nombre"],
                "titulo" : row_from_db["titulo"],
                "num_paginas" : row_from_db["num_paginas"],
                "created_at" : row_from_db["created_at"],
                "updated_at" : row_from_db["created_at"]
            }
            autor.append(libro.Libro(libro_data))
        return autor