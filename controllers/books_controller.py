import re
from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import book_repository
from repositories import author_repository
from models.book import Book

books_blueprint = Blueprint("books",__name__)

@books_blueprint.route("/books")
def books():
    books = book_repository.select_all()
    return render_template("books/index.html", all_books=books)


# NEW - GET /books/new
@books_blueprint.route("/books/new", methods=['GET'])
def new_book():
    authors = author_repository.select_all()
    return render_template("books/new.html", all_authors = authors)

# CREATE - POST /books
@books_blueprint.route("/books", methods=['POST'])
def create_book():
    title = request.form["title"]
    author_id = request.form["author_id"]
    publisher = request.form["publisher"]
    publication_date = request.form["publication_date"]
    author = author_repository.select(author_id)

    book = Book(title, author, publisher, publication_date)
    book_repository.save(book)
    return redirect("/books")

# SHOW - GET /books/<id>
@books_blueprint.route("/books/<id>", methods=['GET'])
def show_book(id):
    book = book_repository.select(id)
    return render_template("books/show.html", book=book)


# DELETE 
@books_blueprint.route("/books/<id>/delete", methods=["POST"])
def delete_book(id):
    book_repository.delete(id)
    return redirect("/books")