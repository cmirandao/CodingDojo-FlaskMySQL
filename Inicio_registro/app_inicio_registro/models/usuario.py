from app_inicio_registro.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX=re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

class Usuario:
    def __init__(self,data):
        self.id=data['id']
        self.nombre=data['nombre']
        self.apellido=data['apellido']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_usuario(cls,data):
        query="SELECT * FROM usuarios WHERE id=%(id)s;"
        result=connectToMySQL("esquema_iniciosesion").query_db(query,data)
        # return result
        return cls(result[0]) #se transforma a objeto para poder manejarlo de manera mas facil

    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre,apellido,email,password) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s);"
        return connectToMySQL("esquema_iniciosesion").query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL("esquema_iniciosesion").query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query="SELECT * FROM usuarios;"
        result=connectToMySQL("esquema_iniciosesion").query_db(query)
        all_usr=[]
        for usr in result:
            all_usr.append(cls(usr))
        return all_usr

    # los métodos estáticos no tienen self o cls pasados a los parámetros
    # necesitamos tomar un parámetro para representar nuestra hamburguesa
    @staticmethod
    def validar_usuario(registro):
        correo={
            "email":registro['email']
        }
        is_valid = True # asumimos que esto es true
        if len(registro['nombre']) < 3:
            flash("Nombre debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['apellido']) < 3:
            flash("Apellido debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['password']) < 8:
            flash("Password debe tener al menos 8 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(correo['email']):
            flash("Email no valido")
            is_valid = False
        elif Usuario.get_by_email(correo):
            flash("Email ya existente")
            is_valid = False
        if registro['password']!= registro['confpassword']:
            flash('Passwords no coinciden')
            is_valid = False
        espacio=False
        mayus=False
        minus=False
        numeros=False
        for contr in registro['password']:
            if contr.isspace()==True:
                espacio=True
            if contr.isdigit()==True:
                numeros=True
            if contr.islower()== True:
                minus=True
            if contr.isupper()== True:
                mayus=True
        if espacio==True:
            flash("Password no debe tener espacios en blanco")
            is_valid = False
        if mayus==False:
            flash("Password deben contener al menos una mayuscula")
            is_valid = False
        if numeros==False:
            flash("Password deben contener al menos un numero")
            is_valid = False
        if minus==False:
            flash("Password deben contener al menos una minuscula")
            is_valid = False
        return is_valid
