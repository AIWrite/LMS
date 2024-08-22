from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted, current_user

from models import db, Book, Section
from cacher import cache

class Books(Resource):
    @auth_token_required
    @roles_accepted("lib")
    def post(self):
        data = request.get_json()
        name = data["name"]
        authors = data["authors"]
        description = data["description"]
        content = data["content"]
        section_id = data["section_id"]
        print(name, description, section_id)
        check = Book.query.filter_by(name=name).first()
        section = Section.query.filter_by(id=section_id).first()
        if not check:
            new_book = Book( name = name, authors = authors, description = description, content = content, section_id = section_id)
            db.session.add(new_book)
            new_book.section_name = section.name
            db.session.commit()
            return make_response(jsonify({"message": "Book is created successfully", "product_id": new_book.id}), 201)
        return make_response(jsonify({"message": "Book is already present"}), 409)
    
    @auth_token_required
    @cache.cached(timeout=10)
    def get(self):
        data = Book.get_all_books()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
    def patch(self):
        data = Book.get_request_books_by_user_id()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)

class specificBook(Resource):
    def put(self, id):
        data = request.get_json()
        name = data["name"]
        authors = data["authors"]
        description = data["description"]
        content = data["content"]
        section_id = data["section_id"]
        book = Book.query.filter_by(id=id).first()
        section = Section.query.filter_by(id=section_id).first()
        if book:
            book.name = name
            book.authors = authors
            book.description = description
            book.content = content
            book.section_id = section_id
            book.section_name = section.name
            db.session.commit()
            return make_response(jsonify({"message": "Book is updated successfully"}), 201)
        return make_response(jsonify({"message": "Book is not present"}), 404)
    
    @auth_token_required
    @roles_accepted("lib")
    def delete(self, id):
        # data = request.get_json()
        id = id
        book = Book.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()    
            return make_response(jsonify({"message": "Book is deleted successfully"}), 201)
        return make_response(jsonify({"message": "Book is not present"}), 404)
    
    def head(self, id):
        print("testpatch")
        data = Book.get_issued_books_by_user_id(id)
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
    def patch(self, id):
        print("testoptions")
        data = Book.get_issued_books_by_lib(id)
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
    def post(self, id):
        print("testpost")
        data = Book.get_requested_books_by_user_id(id)
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
    def get(self):
        print("testget")
        data = Book.get_request_books_by_user_id(id)
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
class specificuserBook(Resource):
    
    def put(self, id):
        print("testpatch")
        data = Book.get_issued_books_by_user_id(id)
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)
    
    def get(self, id):
        print("testpatch")
        data = Book.get_book_by_id(id)
        if data:
            data = data.serialize()
            print(data)
            return make_response(jsonify({"data": data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)