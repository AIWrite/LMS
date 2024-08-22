from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted, current_user
from models import db, Book, User

class Request(Resource):
    @roles_accepted("user")
    def post(self, id):
        data = request.get_json()
        user_id = data["user_id"]
        status = data["status"]
        book = Book.query.filter_by(id=id).first()
        user = User.query.filter_by(id=user_id).first()
        if book:
            book.status = status
            book.user_id = user_id
            book.username = user.username
            book.user_email = user.email
            book.requested  = book.requested + 1
            user = User.query.filter_by(id=user_id).first()
            user.request_count = user.request_count + 1
            user.granted = user.granted + 1
            if user.request_count<=5:
                db.session.commit()
                return make_response(jsonify({"message": "Book requested successfully"}), 201)
            else:
                return make_response(jsonify({"message": "Book requested limit exceeded for user"}), 409)
        return make_response(jsonify({"message": "Book cannot be requested"}), 404)
    
class Return(Resource):
    @roles_accepted("user")
    def post(self, id):
        book = Book.query.filter_by(id=id).first()
        if book:
            books_user_id = book.user_id
            user = User.query.filter_by(id=books_user_id).first()
            user.request_count = user.request_count - 1
            user.revoked = user.revoked + 1
            book.returned  = book.returned + 1
            book.user_id = 0
            book.username = None
            book.user_email = None
            book.status = False
            book.issued_at = None
            book.return_at = None
            db.session.commit()
            return make_response(jsonify({"message": "Book returned successfully"}), 201)
        return make_response(jsonify({"message": "Book cannot be returned"}), 409)
    
class Like(Resource):
    def post(self, id):
        book = Book.query.filter_by(id=id).first()
        if book:
            book.like = book.like + 1
            db.session.commit()
            return make_response(jsonify({"message": "Book liked"}), 201)
        return make_response(jsonify({"message": "Book not fetched"}), 409)