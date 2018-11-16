# =============================================================================
# Author: falseuser
# Created Time: 2018-11-15 17:11:34
# Last modified: 2018-11-16 16:48:13
# Description: controller.py
# =============================================================================
import time
import threading
import collections
from link import ControllerLink
from controller_utils import config, controller_logger
from payload import CommandPayload, DataPayload
from database import DBOperation


class Controller(object):

    def __init__(self):
        controller_id = config.get("default", "controller_id")
        parent_topic = config.get("mqtt", "parent_topic")
        self.link = ControllerLink(controller_id, parent_topic)
        self.link.processing = self.processing
        self.cid = 0
        self.db = DBOperation()
        self.wating_cmd = WatingCommand(time_out=10)
        self.emergency_cids = {-1, -2, -3}

    def _get_worker_id(self, topic):
        topic_list = topic.split(self.parent_topic)
        if topic_list[0] == "":
            try:
                worker_topic = topic_list[1]
                worker_topic_list = worker_topic.split("/")
                return worker_topic_list[1]
            except Exception:
                raise ValueError("Can not get worker id")
        else:
            raise ValueError("Can not get worker id")

    def add_worker(self, worker_id):
        self.link.add_worker(worker_id)

    def remove_worker(self, worker_id):
        self.link.remove_worker(worker_id)

    def processing(self, topic, payload):
        """payload: string"""
        try:
            data_payload = DataPayload.load(payload)
        except Exception as e:
            controller_logger.exception(e)
            return
        worker_id = self._get_worker_id(topic)
        data = data_payload.data
        cid = data_payload.cid
        if cid in self.self.wating_cmd:
            self.db.add_worker_data(worker_id, data)
            controller_logger.info("Get data from {0}.".format(worker_id))
        elif cid in self.emergency_cids:
            controller_logger.warning(
                "Get emergency data from {0}.".format(worker_id))
        else:
            controller_logger.error(
                "Time out or unrecognized data.")

    def send_cmd(self, worker_id, cmd_payload):
        """cmd_payload: CommandPayload instance."""
        payload = cmd_payload.string
        rc = self.link.send(worker_id, payload)
        if rc == 0:
            controller_logger.info(
                "Command(cid={0}) send succeeded.".format(cmd_payload.cid))
        else:
            controller_logger.warning(
                "Command(cid={0}) send failed.".format(cmd_payload.cid))

    def exec_command(self, worker_id, cmd, args=None):
        """cmd: string command."""
        cid = self.cid
        cmd_payload = CommandPayload(cmd, args, cid)
        self.send_cmd(worker_id, cmd_payload)
        self.wating_cmd[cid] = (worker_id, cmd)
        self.cid += 1

    def run(self):
        self.link.start()


class WatingCommand(collections.UserDict):
    """There is a time limit for data"""

    def __init__(self, *args, time_out=5, **kwargs):
        collections.UserDict.__init__(self, *args, **kwargs)
        self.time_out = time_out

    def _delete_timer(self, key):
        """Timeout will be deleted"""
        time.sleep(self.time_out)
        if key in self.data:
            del self.data[key]

    def __setitem__(self, key, item):
        self.data[key] = item
        timer = threading.Thread(target=self._delete_timer, args=(key,))
        timer.start()
