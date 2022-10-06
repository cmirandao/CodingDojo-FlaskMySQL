from flask import render_template,request,redirect
from app_usuarios_crud import app
from app_usuarios_crud.models.usuario import Usuarios

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

@app.route('/show/<int:id>')
def detail_page(id):
    data = {
        'id': id
    }
    return render_template("show_page.html",usuario=Usuarios.get_un_usuario(data))

@app.route('/show_edit/<int:id>')
def mostrar_edicion(id):
    data = {
        'id' : id
    }
    return render_template("edit_page.html",usuario=Usuarios.get_un_usuario(data))
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    data = {
        'id' : id,
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "eml" : request.form["eml"]
    }
    Usuarios.update(data)
    return redirect(f"/show/{id}")

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id': id,
    }
    Usuarios.destroy(data)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404