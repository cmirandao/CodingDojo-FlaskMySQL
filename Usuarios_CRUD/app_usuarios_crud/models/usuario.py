from app_usuarios_crud.config.mysqlconnection import connectToMySQL
class Usuarios:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('esquema_usuarios').query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append( cls(usuario) )
        return usuarios

    @classmethod
    def get_un_usuario(cls,data):
        query = "SELECT * FROM usuarios WHERE id=%(id)s;"
        resultados = connectToMySQL('esquema_usuarios').query_db(query,data)
        return cls(resultados[0])
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios ( nombre , apellido , email ) VALUES ( %(fname)s , %(lname)s , %(eml)s );"
        return connectToMySQL('esquema_usuarios').query_db( query, data )

    @classmethod
    def update(cls,data):
        query = "UPDATE usuarios SET nombre=%(fname)s, apellido=%(lname)s, email=%(eml)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('esquema_usuarios').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('esquema_usuarios').query_db(query,data)