from app_inicio_registro import app
from flask import render_template,request,redirect,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # estamos creando un objeto llamado bcrypt,
# que se realiza invocando la función Bcrypt con nuestra aplicación como argumento
from app_inicio_registro.models.usuario import Usuario
app.secret_key = '@#SSDS%^&G'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/newuser', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    if not Usuario.validar_usuario(request.form):
        return redirect("/")
    user_id = Usuario.save(data)
    session['user_id'] = user_id
    return redirect(f"/dashboard/{session['user_id']}")

@app.route('/dashboard/<int:id>')
def dashboard(id):
    if "user_id" not in session:
        return redirect("/")
    data={
        "id":id
    }
    Usuario.get_usuario(data)
    un_usuario=Usuario.get_usuario(data)
    todos_usuarios=Usuario.get_all()
    return render_template("dashboard.html",todos_usuarios=todos_usuarios,un_usuario=un_usuario)

@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = {
        "email" : request.form["email"]
    }
    user_in_db = Usuario.get_by_email(data)
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
    return redirect(f"/dashboard/{session['user_id']}")

@app.route('/clearsession')
def clear():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404