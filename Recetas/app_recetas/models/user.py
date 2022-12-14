from app_recetas.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX=re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save_user(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('recipe_db').query_db(query,data)

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipe_db').query_db(query)
        users = []
        for usrs in results:
            users.append( cls(usrs) )
        return users

    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL('recipe_db').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipe_db").query_db(query,data)
        # no se encontrĂ³ un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def destroy_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('recipe_db').query_db(query,data)

    @staticmethod
    def validar_usuario(registro):
        correo={
            "email":registro['email']
        }
        is_valid = True # asumimos que esto es true
        if len(registro['first_name']) < 3:
            flash("Nombre debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['last_name']) < 3:
            flash("Apellido debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['password']) < 8:
            flash("Password debe tener al menos 8 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(correo['email']):
            flash("Email no valido")
            is_valid = False
        elif User.get_by_email(correo):
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