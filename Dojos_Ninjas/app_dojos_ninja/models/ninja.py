from app_dojos_ninja.config.mysqlconnection import connectToMySQL

class Ninjas:
    def __init__( self , data ):
        self.id = data['id']
        self.primer_nombre = data['primer_nombre']
        self.apellido = data['apellido']
        self.edad = data['edad']
        self.created_at = data['creado_en']
        self.updated_at = data['actualizado_en']
    @classmethod
    def guardar_ninja(cls,data):
        query="INSERT INTO ninjas(primer_nombre,apellido,edad,dojo_id) VALUES(%(primer_nombre)s,%(apellido)s,%(edad)s,%(dojo_id)s);"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)

    @classmethod
    def get_all_dojos(cls):
        query = "SELECT * FROM ninjas;"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    @classmethod
    def destroy_dojo(cls,data):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query,data)