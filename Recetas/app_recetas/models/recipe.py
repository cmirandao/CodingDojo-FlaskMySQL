from app_recetas.models.user import User
from app_recetas.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.instructions = data['instructions']
        self.recipe_time = data['recipe_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.on_users=[]
        self.one_recipe=[]

    @classmethod
    def save_recipe(cls,data):
        query="INSERT INTO recipes(title,description,instructions,recipe_time,created_at,user_id) VALUES(%(title)s,%(description)s,%(instructions)s,%(recipe_time)s,%(created_at)s,%(user_id)s);"
        return connectToMySQL('recipe_db').query_db(query,data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipe_db').query_db(query)
        recipe = []
        for rcp in results:
            recipe.append( cls(rcp) )
        return recipe

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL('recipe_db').query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET title=%(title)s, description=%(description)s, instructions=%(instructions)s, recipe_time=%(recipe_time)s, created_at=%(created_at)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipe_db').query_db(query,data)

    @classmethod
    def destroy_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipe_db').query_db(query,data)

    @classmethod
    def get_user_recipe(cls):
        query = "SELECT * FROM recipes as r JOIN users as u ON r.user_id = u.id;"
        results = connectToMySQL('recipe_db').query_db(query)
        lista_user=[]
        for row_from_db in results:
            obj_recipe=cls(row_from_db)
            obj_recipe.on_users.append(User(row_from_db))
            lista_user.append(obj_recipe)
        return lista_user

    @classmethod
    def get_user_one_recipe(cls,data):
        query = "SELECT * FROM recipes as r JOIN users as u ON r.user_id = u.id WHERE r.id=%(id)s;"
        results = connectToMySQL('recipe_db').query_db(query,data)
        lista_one_recipe=[]
        for row_from_db in results:
            obj_onerecipe=cls(row_from_db)
            obj_onerecipe.one_recipe.append(User(row_from_db))
            lista_one_recipe.append(obj_onerecipe)
        return lista_one_recipe

    @staticmethod
    def validar_receta(registro):
        is_valid = True # asumimos que esto es true
        if len(registro['title']) < 3:
            flash("Titulo debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['description']) < 3:
            flash("Descripcion debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['instructions']) < 3:
            flash("Instrucciones debe tener al menos 3 caracteres")
            is_valid = False
        return is_valid