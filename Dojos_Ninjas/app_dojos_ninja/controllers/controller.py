from crypt import methods
from app_dojos_ninja.models.ninja import Ninjas
from app_dojos_ninja.models.dojo import Dojos
from flask import render_template,request,redirect
from app_dojos_ninja import app

@app.route('/')
def index():
    return redirect("/dojo")

@app.route('/dojo')
def dojos():
    dojos = Dojos.get_all_dojos()
    return render_template("index.html", todos_dojos = dojos)

@app.route('/create_dojo', methods=["POST"])
def create_user():
    data = {
        "nombre": request.form["nombre"]
    }
    Dojos.guardar_dojo(data)
    return redirect('/')

@app.route('/ninja')
def usuarios():
    dojos = Dojos.get_all_dojos()
    return render_template("crear_ninja.html", todos_dojos = dojos)

@app.route('/create_ninja', methods=["POST"])
def create_ninja():
    data = {
        "primer_nombre": request.form["primer_nombre"],
        "apellido": request.form["apellido"],
        "edad":request.form["edad"],
        "dojo_id":request.form["dojo_id"]
    }
    id=data["dojo_id"]
    Ninjas.guardar_ninja(data)
    return redirect(f"/dojo_show/{id}")

@app.route('/dojo_show/<int:id>')
def dojo_show(id):
    data = {
        'id': id
    }
    un_dojo=Dojos.get_un_dojo(data)
    todos_ninjas=Dojos.get_dojos_y_ninjas(data)
    return render_template("dojo_show.html",todos_ninjas=todos_ninjas,un_dojo=un_dojo)

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404