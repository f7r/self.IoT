# =============================================================================
# Author: falseuser
# File Name: operating_api.py
# Created Time: 2018-10-24 15:01:05
# Last modified: 2018-11-26 17:55:56
# Description:
# =============================================================================
import operations
from flask import Flask
from flask.ext import restful


app = Flask("Operation API")
api = restful.Api(app)
controller_ops = operations.ControllerOperations()


class ControllerStatus(restful.Resource):

    def get(self):
        # return controller status infomation.
        pass


class WorkerStatus(restful.Resource):

    def get(self, worker_id):
        # return a worker status infomation.
        pass


class ControllerConfigOPS(restful.Resource):

    def __init__(self):
        self.parser = restful.reqparse.RequestParser()
        self.parser.add_argument("config", type=dict)

    def get(self):
        return controller_ops.get_global_config()

    def set(self, config):
        args = self.parser.parse_args()
        config = args['config']
        controller_ops.set_global_config(config)
        return "", 201


class WorkerOPS(restful.Resource):

    def delete(self, worker_id):
        controller_ops.unregiste_worker(worker_id)

    def put(self, worker_id):
        controller_ops.register_worker(worker_id)
        return "", 201


class WorkerConfigOPS(restful.Resource):

    def __init__(self):
        self.parser = restful.reqparse.RequestParser()
        self.parser.add_argument("config", type=dict)

    def get(self, worker_id):
        worker_ops = operations.WorkerOperations(worker_id)
        return worker_ops.get_config()

    def post(self, worker_id):
        args = self.parser.parse_args()
        config = args['config']
        worker_ops = operations.WorkerOperations(worker_id)
        worker_ops.set_config(config)
        return "", 201


class WorkerDescriptionOPS(restful.Resource):

    def __init__(self):
        self.parser = restful.reqparse.RequestParser()
        self.parser.add_argument("description", type=str)

    def get(self, worker_id):
        worker_ops = operations.WorkerOperations(worker_id)
        return worker_ops.get_description()

    def post(self, worker_id):
        args = self.parser.parse_args()
        description = args['description']
        worker_ops = operations.WorkerOperations(worker_id)
        worker_ops.set_description(description)
        return "", 201


api.add_resource(ControllerStatus, '/controller/status')
api.add_resource(ControllerConfigOPS, '/controller/config')
api.add_resource(WorkerOPS, '/worker/<string:worker_id>')
api.add_resource(WorkerConfigOPS, '/worker/<string:worker_id>/config')
api.add_resource(
    WorkerDescriptionOPS,
    '/worker/<string:worker_id>/description',
)
api.add_resource(WorkerStatus, '/worker/<string:worker_id>/status')


if __name__ == '__main__':
    app.run(debug=True)
