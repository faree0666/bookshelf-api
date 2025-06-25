from flask import request, jsonify
from models import db, Book

def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({"message": "BookShelf API is up and running"}), 200

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        return jsonify([book.to_shelf() for book in books])

    @app.route('/books/<int:id>', methods=['GET'])
    def get_book(id):
        book = Book.query.get_or_404(id)
        return jsonify(book.to_shelf())

    @app.route('/books', methods=['POST'])
    def add_book():
        data = request.get_json()
        new_book = Book(
            title=data['title'],
            author=data['author'],
            year=data.get('year')
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_shelf()), 201

    @app.route('/books/<int:id>', methods=['PUT'])
    def update_book(id):
        book = Book.query.get_or_404(id)
        data = request.get_json()
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)
        book.read = data.get('read', book.read)
        db.session.commit()
        return jsonify(book.to_shelf())

    @app.route('/books/<int:id>/read', methods=['PATCH'])
    def mark_as_read(id):
        book = Book.query.get_or_404(id)
        book.read = True
        db.session.commit()
        return jsonify(book.to_shelf())

    @app.route('/books/<int:id>', methods=['DELETE'])
    def delete_book(id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return '', 204
