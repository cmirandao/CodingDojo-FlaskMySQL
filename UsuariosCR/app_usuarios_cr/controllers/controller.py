from flask import render_template,request,redirect
from app_usuarios_cr import app
from app_usuarios_cr.models.usuario import Usuarios

@app.route('/')
def index():
    usuarios = Usuarios.get_all()
    print(usuarios)
    return render_template("index.html", todos_usuarios = usuarios)

@app.route('/create_user', methods=["POST"])
def create_user():
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "eml" : request.form["eml"]
    }
    Usuarios.save(data)
    return redirect('/')

@app.route('/crea')
def usuarios():
    return render_template("crear.html")

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404