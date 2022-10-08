from app_dojos_ninja.config.mysqlconnection import connectToMySQL
from app_dojos_ninja.models import ninja

class Dojos:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['creado_en']
        self.updated_at = data['actualizado_en']
        self.ninjas=[]
    
    @classmethod
    def guardar_dojo(cls,data):
        query="INSERT INTO dojos(nombre) VALUES(%(nombre)s);"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)

    @classmethod
    def get_all_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    @classmethod
    def get_un_dojo(cls,data):
        query = "SELECT * FROM dojos WHERE id=%(id)s;"
        resultados = connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)
        return cls(resultados[0])

    @classmethod
    def destroy_dojo(cls,data):
        query = "DELETE FROM dojos WHERE id = %(id)s;"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)

# clase para hacer el join de las 2 tablas
    @classmethod
    def get_dojos_y_ninjas(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)
        dojo=[]
        for row_from_db in results:
            ninja_data = {
                "id" : row_from_db["id"], #id del dojo
                "primer_nombre" : row_from_db["primer_nombre"], #nombre del ninja
                "apellido" : row_from_db["apellido"],#apellido del ninja
                "edad" : row_from_db["edad"],#edad del ninja
                "creado_en" : row_from_db["creado_en"],
                "actualizado_en" : row_from_db["actualizado_en"]
            }
            dojo.append(ninja.Ninjas(ninja_data))
        return dojo