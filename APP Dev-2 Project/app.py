from mailer import mail as email
from flask import jsonify, send_file


def make_celery(server):
    from celery import Celery
    celery = Celery(server.import_name)
    celery.config_from_object('celeryconfig')
    return celery

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object("config.localDev")

    from models import db, user_datastore

    db.init_app(app)
    
    from flask_security import Security
    security = Security(app, user_datastore)

    from flask_restful import Api
    api = Api(app)

    from flask_cors import CORS
    CORS(app)

    from cacher import cache
    cache.init_app(app)

    celeryService = make_celery(app)

    email.init_app(app)

    return app, api, celeryService

app, api_handler, celery_app = create_app()

import tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    "test": {
        "task": "tasks.test",
        "schedule": crontab(hour="01", minute="25")
    },
    "mailuserlogin": {
        "task": "tasks.mailuserlogin",
        "schedule": crontab(hour="01", minute="25")
    },
    "mailuserbooks": {
        "task": "tasks.mailuserbooks",
        "schedule": crontab(hour="01", minute="25")
    },
    "maillib": {
        "task": "tasks.maillib",
        "schedule": crontab(hour="01", minute="25", day_of_month="31")
    }
}
    
from routes.auth import login, register, update
api_handler.add_resource(login, "/api/login")
api_handler.add_resource(register, "/api/register")
api_handler.add_resource(update, "/api/update/<int:id>")

from routes.section import Sections, specificSection
api_handler.add_resource(Sections, "/api/section")
api_handler.add_resource(specificSection, "/api/section/<int:id>")

from routes.book import Books, specificBook, specificuserBook
api_handler.add_resource(Books, "/api/book")
api_handler.add_resource(specificBook, "/api/book/<int:id>")
api_handler.add_resource(specificuserBook, "/api/userbook/<int:id>")

from routes.lib import grant, revoke, allusers
api_handler.add_resource(grant, "/api/grant/<int:id>")
api_handler.add_resource(revoke, "/api/revoke/<int:id>")
api_handler.add_resource(allusers, "/api/allusers")

from routes.user import Request, Return, Like
api_handler.add_resource(Request, "/api/request/<int:id>")
api_handler.add_resource(Return, "/api/return/<int:id>")
api_handler.add_resource(Like, "/api/like/<int:id>")

from routes.asynch import asynch
api_handler.add_resource(asynch, "/api/request/<int:id>")

# @app.route('/test_celery')
# def test_celery():
#     task = tasks.export_ebooks_to_csv.delay()
#     return make_response(task.result, 202)

@app.route('/createcsv')
def createcsv():
    task = tasks.export_ebooks_to_csv.delay()
    while not task.ready():
        pass
    return jsonify({'task-id' : task.id, 'task_status': task.status}), 200

@app.route('/downloadcsv')
def download_csv():
    return send_file("books.csv")

if __name__ == "__main__":
    app.run(debug=True)