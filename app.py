from flask import Flask, render_template, request, redirect, url_for, flash
from library import Library
from models import Book, Member

app = Flask(__name__)
app.secret_key = "dev-key"

lib = Library()

def seed_if_empty():
    if not lib.books and not lib.members:
        lib.add_book("El Principito", "Antoine de Saint-Exupéry", 1943)
        lib.add_book("Cien años de soledad", "Gabriel García Márquez", 1967)
        lib.add_book("Don Quijote de la Mancha", "Miguel de Cervantes", 1605)
        lib.add_member("Ana Pérez")
        lib.add_member("Luis Gómez")
        lib.add_member("María López")

@app.route("/")
def index():
    seed_if_empty()
    totals = {
        "books": len(lib.books),
        "members": len(lib.members),
        "available": len(lib.list_available())
    }
    active_loans = totals["books"] - totals["available"]
    return render_template("index.html", totals=totals, active_loans=active_loans)

@app.route("/books", methods=["GET", "POST"])
def books():
    seed_if_empty()
    if request.method == "POST":
        try:
            t = request.form.get("title", "").strip()
            a = request.form.get("author", "").strip()
            y = int(request.form.get("year", "0"))
            if not t or not a or not y:
                raise ValueError("Título, autor y año son requeridos.")
            lib.add_book(t, a, y)
            flash("Libro agregado.", "success")
            return redirect(url_for("books"))
        except Exception as e:
            flash(str(e), "error")
    q = request.args.get("q", "").strip()
    books = lib.search_books(q) if q else lib.books
    return render_template("books.html", books=books, q=q)

@app.route("/books/return/<int:book_id>", methods=["POST"])
def return_book(book_id: int):
    try:
        lib.return_book(book_id)
        flash("Libro devuelto.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("loans"))

@app.route("/members", methods=["GET", "POST"])
def members():
    seed_if_empty()
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            if not name:
                raise ValueError("El nombre es requerido.")
            lib.add_member(name)
            flash("Miembro agregado.", "success")
            return redirect(url_for("members"))
        except Exception as e:
            flash(str(e), "error")
    return render_template("members.html", members=lib.members)

@app.route("/loans", methods=["GET", "POST"])
def loans():
    seed_if_empty()
    if request.method == "POST":
        try:
            book_id = int(request.form.get("book_id"))
            member_id = int(request.form.get("member_id"))
            lib.lend_book(book_id, member_id)
            flash("¡Préstamo registrado!", "success")
            return redirect(url_for("loans"))
        except Exception as e:
            flash(str(e), "error")

    active = []
    for book in lib.books:
        if not book.available:
            mid = next((mid for bid, mid in lib._loans.items() if bid == book.book_id), None)
            member = lib.find_member_by_id(mid) if mid else None
            active.append({"book": book, "member": member})
    return render_template("loans.html", books=lib.books, members=lib.members, active=active)

if __name__ == "__main__":
    app.run(debug=True)