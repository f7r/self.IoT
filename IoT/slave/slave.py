# =============================================================================
# Author: falseuser
# File Name: slave.py
# Created Time: 2018-09-07 18:00:22
# Last modified: 2018-09-07 18:18:53
# Description:
# =============================================================================
from link import SlaveLink
from source import get_data
# from slave_utils import slave_logger


class Slave(object):

    def __init__(self, slave_id):
        self.slave_id = slave_id
        self.link = SlaveLink(slave_id, "MQTT")
        self.link.processing = self.processing

    def processing(self, payload):
        pass

    def send_data(self):
        data = self.get_data()
        return self.link.send(data)

    def get_data(self):
        return get_data()
