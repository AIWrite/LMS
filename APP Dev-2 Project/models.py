from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, event
from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from datetime import datetime

db = SQLAlchemy()

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    granted = Column(Integer, default=0, nullable=True)
    revoked = Column(Integer, default=0, nullable=True)
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    request_count = Column(Integer, default=0)
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'granted': self.granted,
            'revoked': self.revoked
        }
    
    def get_all_users():
        return User.query.all()
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    
class Section(db.Model):
    __tablename__ = 'section'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())
    books = relationship('Book', backref='section', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'books': [book.serialize() for book in self.books] if self.books else 'No books found'
        }
    
    def get_all_sections():
        data = Section.query.all()
        if data:
            return data
        return False
    
    def get_section_by_id(id):
        return Section.query.filter_by(id=id).first()
    
    def lib_delete(id):
        section = Section.query.filter_by(id=id).first()
        db.session.delete(section)
        db.session.commit()
        if Section.query.filter_by(id=id).first() == None:
            return True
        return False


class Book(db.Model):
    __tablename__ = 'book'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    authors = Column(String(255))
    description = Column(String(255))
    content = Column(String(255))
    requested = Column(Integer, default=0, nullable=True)
    returned = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())
    status = Column(Boolean(), default=False)
    section_id = Column(Integer(), ForeignKey('section.id'))
    section_name = Column(String(255))
    user_id = Column(Integer(), default=0)
    username = Column(String(255))
    user_email = Column(String(255))
    like = Column(Integer(), default=0)
    issued_at = Column(DateTime(), nullable=True)
    return_at = Column(DateTime(), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authors': self.authors,
            'description': self.description,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'section_id': self.section_id,
            'section_name': self.section_name,
            'user_id': self.user_id,
            'status': self.status,
            'username': self.username,
            'user_email': self.user_email,
            'issued_at': self.issued_at,
            'like': self.like,
            'return_at': self.return_at,
            'requested': self.requested,
            'returned': self.returned
        }
    
    def get_all_books():
        data = Book.query.all()
        if data:
            return data
        return False
    
    def get_book_by_id(id):
        return Book.query.filter_by(id=id).first()
    
    def get_books_by_user_id(id):
        data = Book.query.filter_by(user_id = 0, status = True).all()
        if data:
            return data
        return False
    
    def get_issued_books_by_user_id(id):
        data = Book.query.filter_by(user_id = id, status = True).all()
        if data:
            return data
        return False
    
    def get_issued_books_by_lib(id):
        data = Book.query.filter(Book.user_id != 0, Book.status == True).all()
        if data:
            return data
        return False
    
    def get_requested_books_by_user_id(id):
        data = Book.query.filter(Book.user_id != 0, Book.status == False).all()
        if data:
            return data
        return False
    
    def get_request_books_by_user_id():
        data = Book.query.filter_by(user_id = 0, status = False).all()
        if data:
            return data
        return False
    
    def lib_delete(id):
        book = Book.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        if Book.query.filter_by(id=id).first() == None:
            return True
        return False