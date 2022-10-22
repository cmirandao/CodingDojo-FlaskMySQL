from app_muro.models.msje import Msje
from app_muro import app
from flask import render_template,request,redirect,session,flash
from app_muro.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = '@#SSDS%^&G'

@app.route('/')
def index():
    return render_template("index.html")

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
    session['user_id'] = user_in_db.iduser
    return redirect("/wall")

@app.route('/wall')
def wall():
    if "user_id" not in session:
        return redirect("/")
    id=session['user_id']
    data={
        "iduser":id
    }
    data2={
        "destinatario":id
    }
    data3={
        "remitente":id
    }
    un_usuario=User.get_one_user(data)
    msjes_user=Msje.get_msjes_one_user(data2)
    msjusr=len(msjes_user)
    all_users=User.get_all_users()
    countmsje=Msje.get_count_msjes(data3)
    contm=countmsje[0]['cont']
    return render_template("msjes.html",msjes_user=msjes_user,un_usuario=un_usuario,msjusr=msjusr,all_users=all_users,contm=contm)

@app.route('/create', methods=["POST"])
def create():
    valor=request.form['tipo']
    if valor == "user":
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],
            "email": request.form['email'],
            "password" : pw_hash
        }
        if not User.validar_usuario(request.form):
            return redirect("/")
        user_id = User.save_user(data)
        session['user_id'] = user_id
        flash("Usuario creado correctamente, ahora puedes logearte")
        return redirect('/')
    elif valor == "msje":
        data = {
            "mensaje":request.form["mensaje"],
            "remitente":session['user_id'],
            "destinatario":request.form['usuario']
        }
        if not Msje.validar_msje(request.form):
            return redirect("/wall")
        Msje.save_msje(data)
        flash("Mensaje enviado correctamente")
        return redirect('/wall')

@app.route('/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        'idmsje': id,
    }
    Msje.destroy_msje(data)
    flash("Mensaje borrado correctamente")
    return redirect('/wall')

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