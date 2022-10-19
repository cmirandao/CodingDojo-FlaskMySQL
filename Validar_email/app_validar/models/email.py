from app_validar.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX=re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

class Email:
    def __init__( self , data ):
        self.id = data['id']
        self.email=data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_email(cls,data):
        query="INSERT INTO emails(email) VALUES(%(email)s);"
        return connectToMySQL('validar_db').query_db(query,data)

    @classmethod
    def delete_email(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL('validar_db').query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        result = connectToMySQL("validar_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_emails(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL('validar_db').query_db(query)
        emails = []
        for eml in results:
            emails.append( cls(eml) )
        return emails

    @classmethod
    def get_one_email(cls,data):
        query = "SELECT * FROM emails WHERE id=%(id)s;"
        results = connectToMySQL('validar_db').query_db(query,data)
        return cls(results[0])

    @classmethod
    def last_id(cls):
        query="SELECT * FROM emails order by id desc limit 1;"
        return connectToMySQL('validar_db').query_db(query)

    @staticmethod
    def validar_email(registro):
        correo={
            "email":registro['email']
        }
        is_valid = True # asumimos que esto es true
        if not EMAIL_REGEX.match(correo['email']):
            flash("Email no valido")
            is_valid = False
        elif Email.get_by_email(correo):
            flash("Email ya existente")
            is_valid = False
        return is_valid