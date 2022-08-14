from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
from flask_app.models.user import User
from flask_app.models.book import Book



@app.route("/dashboard")
def dashboard():
    #user should be logged in to view the page
    if "user_id" not in session:
        flash("You must be logged in to access the page")
        return redirect("/")
    user_data = {
            "id": session["user_id"]
        }
    user = User.get_user_by_id(user_data)

    books = Book.get_all()
    return render_template("dashboard.html", user=user, books=books)


@app.route("/show/<int:id>")
def show_book(id):
    # user should be logged in to view the page
    if "user_id" not in session:
        flash("You must be logged in to access the page")
        return redirect("/")
    user_data = {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(user_data)
    book_data = {
        "id": id
    }
    book = Book.get_one(book_data)
    return render_template("show_book.html", user=user, book=book)


# create new book- display route
@app.route("/book/new")
def new_create_book_form():
    # user should be logged in to view the page
    if "user_id" not in session:
        flash("You must be logged in to access the page")
        return redirect("/")
    user_data = {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(user_data)
    return render_template("create_book.html", user=user)


# create new book - process route
@app.route("/book/create", methods=["POST"])
def create_book():
    # form validation
    if not Book.validate_create_book(request.form):
        return redirect("/book/new")
    Book.create_book(request.form)
    return redirect("/dashboard")



# edit - diplay route
@app.route("/book/<int:id>/edit")
def show_edit_form(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    book_edit = {
        "id": id
    }
    book = Book.get_one(book_edit)
    # only book creator can access the page
    if (book.user_id != user.id):
        flash(f"Unauthorized access to edit review with id {id}")
        return redirect("/dashboard")
    return render_template("edit_book.html", book=book, user=user)


# edit - process route
@app.route("/book/<int:id>/update", methods=["POST"])
def update(id):
    # form validation
    if not Book.validate_create_book(request.form):
        # need to pass id argument to the route
        return redirect(url_for("show_edit_form", id=id))
    Book.update(request.form)
    return redirect("/dashboard")


@app.route("/book/<int:id>/read", methods=["POST"])
def read(id):
    Book.read(request.form)
    return redirect("/dashboard")


# remove from read list - remove process route
@app.route("/book/<int:id>/remove", methods=["POST"])
def remove(id):
    Book.remove(request.form)
    return redirect("/dashboard")


# delete - delete process route
@app.route("/book/<int:id>/delete", methods=["POST"])
def delete(id):
    Book.delete(request.form)
    return redirect("/dashboard")