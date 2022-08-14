from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Book:
    db = "bookshelves"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.author = data["author"]
        self.description = data["description"]
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.readers = []
        self.reader_ids = []

    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM books 
            JOIN users as creators ON books.user_id = creators.id
            LEFT JOIN read_books ON read_books.book_id = books.id
            LEFT JOIN users as readers ON read_books.user_id = readers.id;'''
        results = connectToMySQL(cls.db).query_db(query)
        
        books = []

        for row in results:
            new_book = True

            reader_data = {
                "id": row["readers.id"],
                "first_name": row["readers.first_name"],
                "last_name": row["readers.last_name"],
                "email": row["readers.email"],
                "password": row["readers.password"],
                "created_at": row["readers.created_at"],
                "updated_at": row["readers.updated_at"],
            }

            number_of_books = len(books)
            if number_of_books > 0:
                last_book = books[number_of_books-1]

                if last_book.id == row["id"]:
                    last_book.reader_ids.append(row["readers.id"])
                    last_book.readers.append(User(reader_data))
                    new_book = False
            
            if new_book:
                book = cls(row)
                user_data = {
                    "id": row["readers.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["readers.created_at"],
                    "updated_at": row["readers.updated_at"],
                }
                user = User(user_data)
                book.user=user

                if row["readers.id"]:
                    book.reader_ids.append(row["readers.id"])
                    book.readers.append(User(reader_data))
                
                books.append(book)
        return books

    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM books 
            JOIN users as creators ON books.user_id = creators.id
            LEFT JOIN read_books ON read_books.book_id = books.id
            LEFT JOIN users as readers ON read_books.user_id = readers.id
            WHERE books.id = %(id)s;
            '''
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        
        new_book = True
        for row in results:
            if new_book:
                book = cls(row)
                # create a user object
                user_data = {
                "id": row["creators.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["creators.created_at"],
                "updated_at": row["creators.updated_at"],
                }
                creator = User(user_data)
                book.creator = creator
                new_book = False

            if row["readers.id"]:
                reader_data = {
                    "id": row["readers.id"],
                    "first_name": row["readers.first_name"],
                    "last_name": row["readers.last_name"],
                    "email": row["readers.email"],
                    "password": row["readers.password"],
                    "created_at": row["readers.created_at"],
                    "updated_at": row["readers.updated_at"],
                }
                reader = User(reader_data)
                book.reader_ids.append(row["readers.id"])
                book.readers.append(reader)
        return book

    
    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books(title, author, description, user_id) VALUES(%(title)s, %(author)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    # @classmethod
    # def create_review(cls, data):
    #     query = "INSERT INTO books(user_id, book_id, review, rating, completed_at) VALUES(%(user_id)s, %(book_id)s, %(review)s, %(rating)s);"
    #     return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title=%(title)s, author=%(author)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def read(cls, data):
        query = "INSERT INTO read_books(user_id, book_id) VALUES(%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def remove(cls, data):
        query = "DELETE FROM read_books WHERE user_id=%(user_id)s AND book_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_create_book(book):
        is_valid = True
        if len(book["title"]) < 1:
            flash("Title must be at least 1 character.")
            is_valid = False
        if len(book["author"]) < 1:
            flash("Author must be at least 1 character.")
            is_valid = False
        if len(book["description"]) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        return is_valid

    # @staticmethod
    # def validate_create_review(review):
    #     is_valid = True
    #     # if len(review["review"]) < 1:
    #     #     flash("Title must be at least 1 character.")
    #     #     is_valid = False
    #     # if len(book["author"]) < 1:
    #     #     flash("Author must be at least 1 character.")
    #     #     is_valid = False
    #     if len(review["review"]) < 10:
    #         flash("Review must be at least 10 characters.")
    #         is_valid = False
    #     return is_valid






