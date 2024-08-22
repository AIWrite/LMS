from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted
from datetime import datetime, timedelta
from models import db, user_datastore, Book, User

class grant(Resource):
    @roles_accepted("lib")
    def post(self, id):
        data = request.get_json()
        status = data["status"]
        book = Book.query.filter_by(id=id).first()
        libr = User.query.filter_by(id=1).first()
        if book:
            books_user_id = book.user_id
            user = User.query.filter_by(id=books_user_id).first()
            user.request_count = user.request_count - 1
            libr.granted = libr.granted + 1
            book.requested  = book.requested + 1
            book.status = status
            book.issued_at = datetime.now()
            book.return_at = book.issued_at + timedelta(days=7)
            db.session.commit()
            return make_response(jsonify({"message": "Book issued"}), 201)
        return make_response(jsonify({"message": "Book cannot be issued"}), 409)
        
class revoke(Resource):
    @roles_accepted("lib")
    def post(self, id):
        data = request.get_json()
        status = data["status"]
        book = Book.query.filter_by(id=id).first()
        libr = User.query.filter_by(id=1).first()
        if book:
            books_user_id = book.user_id
            user = User.query.filter_by(id=books_user_id).first()
            user.request_count = user.request_count - 1
            libr.revoked = libr.revoked + 1
            book.returned  = book.returned + 1
            book.user_id = 0
            book.username = None
            book.user_email = None
            book.status = status
            book.issued_at = None
            book.return_at = None
            db.session.commit()
            return make_response(jsonify({"message": "Book revoked successfully"}), 201)
        return make_response(jsonify({"message": "Book is granted to ghost"}), 404)
    
    def delete(self, id):
        id = id
        user = User.query.filter_by(id=id).first()
        books = Book.query.filter_by(user_id = id).all()
        if user:
            if books:
                for book in books:
                    book.user_id = 0
                    book.status = False
                    book.username = None
                    book.user_email = None
                    book.issued_at = None
                    book.return_at = None
                    db.session.commit()
            db.session.delete(user)
            db.session.commit()    
            return make_response(jsonify({"message": "User deleted successfully"}), 201)
        return make_response(jsonify({"message": "User not present"}), 404)
    
class allusers(Resource):
    @roles_accepted("lib")
    def get(self):
        data = User.get_all_users()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No User found"}), 404)
    
