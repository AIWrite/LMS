from flask_restful import Resource
from flask import jsonify
import tasks

class asynch(Resource):

    def post(self):
        task = tasks.export_ebooks_to_csv.delay()
        return jsonify({'task_id': str(task.id)}), 202

    def get(self, task_id):
        task = tasks.export_ebooks_to_csv.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state
            }
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result
            }
        else:
            response = {
                'state': task.state,
                'error': str(task.info)
            }
        return jsonify(response)