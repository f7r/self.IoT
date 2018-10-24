# =============================================================================
# Author: falseuser
# File Name: operating_api.py
# Created Time: 2018-10-24 15:01:05
# Last modified: 2018-10-24 15:12:16
# Description:
# =============================================================================
from flask import Flask
from flask.ext import restful


app = Flask("Operation API")
api = restful.Api(app)


class ControllerStatus(restful.Resource):

    def get(self):
        # return controller status infomation.
        pass


class WorkerStatus(restful.Resource):

    def get(self, worker_id):
        # return a worker status infomation.
        pass


api.add_resource(ControllerStatus, '/controller/status')
api.add_resource(WorkerStatus, '/worker/<string:worker_id>/status')


if __name__ == '__main__':
    app.run(debug=True)
