from app import create_app
from models import db, user_datastore

app, _, _ = create_app()

def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='lib', description='Librarian')
    user_datastore.find_or_create_role(name='user', description='General User')
    db.session.commit()

    if not user_datastore.find_user(email="lib@a.com"):
        admin_user=user_datastore.create_user(email="lib@a.com", password="lib", username="lib")
        user_datastore.add_role_to_user(admin_user, "lib")

    db.session.commit()