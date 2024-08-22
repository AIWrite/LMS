from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, roles_accepted

from models import db, Section, Book
from cacher import cache

class Sections(Resource):
    @auth_token_required
    @roles_accepted("lib")
    def post(self):
        data = request.get_json()
        name = data["name"]
        description = data["description"]
        
        check = Section.query.filter_by(name=name).first()
        if not check:
            new_sec = Section()
            new_sec.name = name
            new_sec.description = description
            db.session.add(new_sec)
            db.session.commit()
            return make_response(jsonify({"message": "Section is created successfully", "cate_id": new_sec.id}), 201)
        return make_response(jsonify({"message": "Section is already present"}), 409)
     

    @auth_token_required
    # @cache.cached(timeout=10)
    def get(self):
        data = Section.get_all_sections()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No section found"}), 404)
    
    
class specificSection(Resource):
    @auth_token_required
    @roles_accepted("lib")
    def put(self, id):
        data = request.get_json()
        name = data["name"]
        description = data["description"]
        sec = Section.query.filter_by(id=id).first()
        books = Book.query.filter_by(section_id=id).all()
        if sec:
            sec.name = name
            sec.description = description
            if books:
                for book in books:
                    book.section_name = name
                    db.session.commit()
            db.session.commit()
            return make_response(jsonify({"message": "Section is updated successfully", "cate_id": sec.id}), 201)
        return make_response(jsonify({"message": "Section is not present"}), 404)
    
    @auth_token_required
    @roles_accepted("lib")
    def delete(self, id):
        # data = request.get_json()
        id = id
        sec = Section.query.filter_by(id=id).first()
        books = Book.query.filter_by(section_id=id).all()
        if sec:
            if books:
                for book in books:
                    book.section_id = None
                    book.section_name = None
                    db.session.commit()
            db.session.delete(sec)
            db.session.commit()    
            return make_response(jsonify({"message": "Section is deleted successfully", "cate_id": sec.id}), 201)
        return make_response(jsonify({"message": "Section is not present"}), 404)
    
    def patch(self, id):
        print("test")
        sec = Section.query.filter_by(id=id).first()
        return make_response(jsonify({"message": "Section found", "id": sec.id}), 200)
