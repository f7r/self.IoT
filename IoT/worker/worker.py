# =============================================================================
# Author: falseuser
# File Name: worker.py
# Created Time: 2018-09-07 18:00:22
# Last modified: 2018-09-12 11:21:57
# Description:
# =============================================================================
from link import WorkerLink
from source import get_data
from worker_utils import config


class Worker(object):

    def __init__(self):
        worker_id = config.get("default", "worker_id")
        parent_topic = config.get("mqtt", "parent_topic")
        self.link = WorkerLink(worker_id, parent_topic)
        self.link.processing = self.processing

    def processing(self, payload):
        pass

    def send_data(self):
        data = self.get_data()
        return self.link.send(data)

    def get_data(self):
        return get_data()


if __name__ == "__main__":
    s = Worker()
