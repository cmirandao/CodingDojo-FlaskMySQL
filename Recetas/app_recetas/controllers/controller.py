from calendar import day_abbr
from datetime import date, datetime
from app_recetas.models.recipe import Recipe
from app_recetas import app
from flask import render_template,request,redirect,session,flash
from app_recetas.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = '@#SSDS%^&G'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recipes/new')
def new_recipe():
    if "user_id" not in session:
        return redirect("/")
    id=session['user_id']
    data={
        "id":id
    }
    un_usuario=User.get_one_user(data)
    now=datetime.now().strftime('%Y-%m-%d')
    return render_template("new_recipe.html",un_usuario=un_usuario,now=now)

@app.route('/create', methods=["POST"])
def create():
    valor=request.form['tipo']
    if valor == "user":
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password" : pw_hash
        }
        if not User.validar_usuario(request.form):
            return redirect("/")
        user_id = User.save_user(data)
        session['user_id'] = user_id
        flash("Usuario creado correctamente, ahora puedes logearte")
        return redirect('/')
    elif valor == "recipe":
        data = {
            "title":request.form["title"],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "recipe_time":request.form["recipe_time"],
            "created_at":request.form["created_at"],
            "user_id":session['user_id']
        }
        if not Recipe.validar_receta(request.form):
            return redirect("/recipes")
        Recipe.save_recipe(data)
        flash("Receta creada correctamente")
        return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = {
        "email" : request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Email/Password erroneos")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Email/Password erroneos")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    return redirect("/recipes")

@app.route('/recipes')
def recipes():
    if "user_id" not in session:
        return redirect("/")
    id=session['user_id']
    data={
        "id":id
    }
    # User.get_one_user(data)
    un_usuario=User.get_one_user(data)
    todas_recetas=Recipe.get_user_recipe()
    return render_template("recipes.html",todas_recetas=todas_recetas,un_usuario=un_usuario)

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    iduser=session['user_id']
    newdata={"id":iduser}
    data={
        "id":id
    }
    un_usuario=User.get_one_user(newdata)
    todas_recetas=Recipe.get_user_one_recipe(data)
    return render_template("view_recipe.html",todas_recetas=todas_recetas,un_usuario=un_usuario)

@app.route('/recipes/edit/<int:id>')
def mostrar_edicion(id):
    if "user_id" not in session:
        return redirect("/")
    iduser=session['user_id']
    newdata={"id":iduser}
    data = {
        'id' : id
    }
    un_usuario=User.get_one_user(newdata)
    una_receta=Recipe.get_one_recipe(data)
    fecha=str(una_receta.created_at)
    now=datetime.now().strftime('%Y-%m-%d')
    checkedsi=""
    checkedno=""
    if una_receta.recipe_time==1:
        checkedsi="checked"
    if una_receta.recipe_time==2:
        checkedno="checked"
    return render_template("edit_recipe.html",receta=Recipe.get_one_recipe(data),un_usuario=un_usuario,fecha=fecha,checkedsi=checkedsi,checkedno=checkedno,now=now)

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        'id' : id,
        "title": request.form["title"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "recipe_time" : request.form["recipe_time"],
        "created_at" : request.form["created_at"]
    }
    Recipe.update(data)
    return redirect("/recipes")

@app.route('/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        'id': id,
    }
    Recipe.destroy_recipe(data)
    flash("Receta borrada correctamente")
    return redirect('/recipes')

@app.route('/clearsession')
def clear():
    if "user_id" not in session:
        return redirect("/")
    session.clear()
    return redirect('/')

@app.errorhandler(405)
def page_not_found(e):
    return "Ruta erronea... Inténtalo otra vez.", 405

@app.errorhandler(404)
def page_not_found(e):
    return "Ruta erronea. Inténtalo otra vez.", 404