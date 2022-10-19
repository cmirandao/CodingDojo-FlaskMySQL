from app_encuesta_dojo.models.dojo import Dojo
from app_encuesta_dojo import app
from flask import render_template,redirect, request, flash
app.secret_key = '@#SSDS%^&G' 

@app.route('/')
def inicio():
    all_dojos=Dojo.get_all_dojos()
    return render_template('index.html',all_dojos=all_dojos)

@app.route('/process', methods=["POST"])
def create():
    data = {
        "nombre":request.form["nombre"],
        "ubicacion":request.form["ubicacion"],
        "idioma":request.form["idioma"],
        "comentario":request.form["comentario"]
    }
    if not Dojo.validar_dojo(request.form):
        return redirect("/")
    Dojo.save_dojo(data)
    flash("Encuesta registrada correctamente")
    return redirect('/result')

@app.route('/result', methods=['GET'])
def result():
    iddojo=Dojo.last_id()[0]['id']
    data={
        "id":iddojo
    }
    un_dojo=Dojo.get_one_dojo(data)
    return render_template('result.html',un_dojo=un_dojo)

@app.route('/volver')
def volver():
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404