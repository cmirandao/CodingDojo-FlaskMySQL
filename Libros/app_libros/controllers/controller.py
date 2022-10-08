from crypt import methods
from app_libros.models.libro import Libro
from app_libros.models.autor import Autor
from flask import render_template,request,redirect
from app_libros import app

@app.route('/')
def index():
    return redirect("/authors")

@app.route('/authors')
def autores():
    autores = Autor.get_all_autor()
    return render_template("authors.html", todos_autores = autores)

@app.route('/create', methods=["POST"])
def create():
    valor=request.form['tipo']
    if valor == "autor":
        data = {
            "nombre": request.form["nombre"]
        }
        Autor.guardar_autor(data)
        return redirect('/authors')
    else:
        data = {
            "titulo":request.form["titulo"],
            "num_paginas":request.form["num_paginas"]
        }
        Libro.guardar_libro(data)
        return redirect('/books')

@app.route('/save_fav',methods=["POST"])
def save_fav():
    valor=request.form['tipo']
    data={
        "autor_id":request.form["autor_id"],
        "libro_id":request.form["libro_id"]
    }
    autor_id=data["autor_id"]
    libro_id=data["libro_id"]
    Autor.guardar_favorito(data)
    if valor=="libro_fav":
        return redirect(f"/books/{libro_id}")
    else:
        return redirect(f"/authors/{autor_id}")

@app.route('/books/<int:id>')
def book_show(id):
    data = {
        'id': id
    }
    un_libro=Libro.get_un_libro(data)
    todos_autores=Autor.ver_no_favoritos(data)
    favoritos_autor=Libro.get_autores_libros(data)
    return render_template("show_book.html",todos_autores=todos_autores,un_libro=un_libro,favoritos_autor=favoritos_autor)

@app.route('/books')
def books():
    libros = Libro.get_all_libros()
    return render_template("books.html", todos_libros = libros)

@app.route('/authors/<int:id>')
def author_show(id):
    data = {
        'id': id
    }
    un_autor=Autor.get_un_autor(data)
    todos_libros=Libro.ver_no_favoritos(data)
    favoritos_libro=Autor.get_libros_autores(data)
    return render_template("show_authors.html",todos_libros=todos_libros,un_autor=un_autor,favoritos_libro=favoritos_libro)

@app.errorhandler(404)
def page_not_found(e):
    return "¡Lo siento! No hay respuesta. Inténtalo otra vez.", 404