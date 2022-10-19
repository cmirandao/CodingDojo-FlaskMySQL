from app_validar import app
from app_validar.models.email import Email
from flask import render_template,request,redirect,flash
app.secret_key = '@#SSDS%^&G'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=["POST"])
def create():
    data = {
        "email":request.form["email"]
    }
    if not Email.validar_email(request.form):
        return redirect("/")
    Email.save_email(data)
    idemail=Email.last_id()[0]['id']
    data={
        "id":idemail
    }
    un_dojo=Email.get_one_email(data)
    flash("El email que acabas de ingresar ("+un_dojo.email+") es un email valido. ¡Gracias!")
    return redirect('/success')

@app.route('/success', methods=['GET'])
def success():
    all_email=Email.get_all_emails()
    return render_template('success.html',all_email=all_email)

@app.route('/delete/<int:id>')
def delete(id):
    data={
        "id":id
    }
    Email.delete_email(data)
    flash("Email borrado exitosamente")
    return redirect('/success')

@app.route('/volver')
def volver():
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404