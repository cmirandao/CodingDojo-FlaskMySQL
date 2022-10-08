from app_libros.config.mysqlconnection import connectToMySQL
from app_libros.models import autor

class Libro:
    def __init__( self , data ):
        self.id = data['id']
        self.titulo = data['titulo']
        self.num_paginas = data['num_paginas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.autores = []
    @classmethod
    def guardar_libro(cls,data):
        query="INSERT INTO libros(titulo,num_paginas) VALUES(%(titulo)s,%(num_paginas)s);"
        return connectToMySQL('esquema_libros').query_db(query,data)

    @classmethod
    def ver_no_favoritos(cls,data):
        query="select * from libros where libros.id not in (select libro_id from favoritos where autor_id=%(id)s);"
        results=connectToMySQL('esquema_libros').query_db(query,data)
        libro_no_fav=[]
        for lbfav in results:
            libro_no_fav.append(cls(lbfav))
        return libro_no_fav

    @classmethod
    def get_all_libros(cls):
        query = "SELECT * FROM libros;"
        results = connectToMySQL('esquema_libros').query_db(query)
        libros = []
        for lbr in results:
            libros.append( cls(lbr) )
        return libros

    @classmethod
    def get_un_libro(cls,data):
        query = "SELECT * FROM libros WHERE id=%(id)s;"
        resultados = connectToMySQL('esquema_libros').query_db(query,data)
        return cls(resultados[0])

    @classmethod
    def destroy_libro(cls,data):
        query = "DELETE FROM libros WHERE id = %(id)s;"
        return connectToMySQL('esquema_libros').query_db(query,data)

    @classmethod
    def get_autores_libros(cls,data):
        query = """SELECT * FROM libros LEFT JOIN favoritos ON favoritos.libro_id = libros.id
        LEFT JOIN autores ON favoritos.autor_id = autores.id WHERE libros.id = %(id)s"""
        results = connectToMySQL('esquema_libros').query_db(query,data)
        libro = []
        for row_from_db in results:
            autor_data = {
                "id" : row_from_db["autores.id"],
                "nombre" : row_from_db["nombre"],
                "created_at" : row_from_db["created_at"],
                "updated_at" : row_from_db["updated_at"]
            }
            libro.append(autor.Autor(autor_data))
        return libro