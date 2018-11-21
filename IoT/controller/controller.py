# =============================================================================
# Author: falseuser
# Created Time: 2018-11-15 17:11:34
# Last modified: 2018-11-21 18:26:38
# Description: controller.py
# =============================================================================
import time
import json
import threading
import collections
from xmlrpc.server import SimpleXMLRPCServer
from link import ControllerLink
from controller_utils import config, controller_logger
from payload import CommandPayload, DataPayload
from database import DBOperation


class Controller(object):

    def __init__(self):
        self.db = DBOperation()
        self.worker_mgr = WorkerManager()
        self.task_mgr = WorkerTaskManager(self.worker_mgr.exec_command)
        self.rpc_server = SimpleXMLRPCServer(("localhost", 8088))
        self.rpc_server.register_instance(ControllerRPCHandler(self))

    def add_worker(self, worker_id, description):
        self.db.add_worker(worker_id, description)
        self.db.add_worker_config(worker_id)
        self.worker_mgr.link_worker(worker_id)

    def remove_worker(self, worker_id):
        self.db.remove_worker(worker_id)
        self.worker_mgr.unlink_worker(worker_id)

    def set_worker_config(self, worker_id, config):
        self.db.set_worker_config_content(worker_id, config)

    def get_worker_data(self, worker_id, cmd, time_limit):
        return self.db.get_worker_data(worker_id, cmd, time_limit)

    def _link_workers(self):
        workers_id_list = self.db.get_registered_workers_id_list()
        for worker_id in workers_id_list:
            self.worker_mgr.link_worker(worker_id)

    def run(self):
        self.worker_mgr.run()
        self._link_workers()
        self.task_mgr.run()
        controller_logger.info("Controller Started.")
        self.rpc_server.serve_forever()  # The process is blocked here.


class ControllerRPCHandler(object):

    def __init__(self, controller):
        self.controller = controller
        self.worker_mgr = self.controller.worker_mgr
        self.db = self.controller.db

    def add_worker(self, worker_id, description=""):
        self.controller.add_worker(worker_id, description)
        return 0

    def remove_worker(self, worker_id):
        self.controller.remove_worker(worker_id)
        return 0

    def get_workers_id_list(self):
        return self.db.get_registered_workers_id_list()

    def get_workers_count(self):
        return self.db.get_registered_workers_count()

    def send_cmd(self, worker_id, cmd):
        self.worker_mgr.exec_command(worker_id, cmd)
        return 0

    def get_worker_data(self, worker_id, cmd):
        return self.controller.get_worker_data(worker_id, cmd, "last")

    def get_worker_data1(self, worker_id, cmd):
        return self.controller.get_worker_data(worker_id, cmd, "24h")

    def set_worker_config(self, worker_id, config):
        self.controller.set_worker_config(worker_id, config)
        return 0

    def get_temperature_last(self, worker_id):
        cmd = "get_temperature"
        return self.controller.get_worker_data(worker_id, cmd, "last")

    def get_temperature_24h(self, worker_id):
        cmd = "get_temperature"
        return self.controller.get_worker_data(worker_id, cmd, "24h")


class WorkerTaskManager(object):

    def __init__(self, exec_func):
        self.db = DBOperation()
        self.exec_func = exec_func
        self.removed_workers = set()

    def periodic_cmd(self, worker_id, cmd, period):
        """exection command periodic."""
        while True:
            time.sleep(period)
            self.exec_func(worker_id, cmd)
            if worker_id in self.removed_workers:
                break

    def run_worker_task(self, worker_id, config):
        """
        config_dict: {
            "periodic": {
                "command1": 30,
                "command2": 40,
            }
        }
        """
        config_dict = json.loads(config)
        if "periodic" in config_dict:
            periodic_task = config_dict["periodic"]
            for cmd in periodic_task:
                period = periodic_task[cmd]
                t = threading.Thread(
                    target=self.periodic_cmd,
                    args=(worker_id, cmd, period),
                )
                t.start()

    def run(self):
        """run workers periodic task"""
        workers_id_list = self.db.get_registered_workers_id_list()
        for worker_id in workers_id_list:
            self.start_worker_task(worker_id)

    def start_worker_task(self, worker_id):
        if worker_id in self.removed_workers:
            self.removed_workers.remove(worker_id)
        worker_config = self.db.get_worker_config_content(worker_id)
        self.run_worker_task(worker_id, worker_config)

    def stop_worker_task(self, worker_id):
        self.removed_workers.add(worker_id)


class WorkerManager(object):
    """Manage and connection with workers."""

    def __init__(self):
        self.controller_id = config.get("default", "controller_id")
        self.parent_topic = config.get("mqtt", "parent_topic")
        self.link = ControllerLink(self.controller_id, self.parent_topic)
        self.link.processing = self.processing
        self.cid = 0
        self.db = DBOperation()
        self.wating_cmd = WatingCommand(time_out=20)
        self.emergency_cids = {-1, -2, -3}
        self._send = {}
        self._received = {}

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

    def link_worker(self, worker_id):
        self.link.add_worker(worker_id)
        self._send[worker_id] = 0
        self._received[worker_id] = 0

    def unlink_worker(self, worker_id):
        self.link.remove_worker(worker_id)
        del self._send[worker_id]
        self._received[worker_id]

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
        if cid in self.wating_cmd:
            if self.wating_cmd[cid][0] == worker_id:
                self._received[worker_id] += 1
                cmd = self.wating_cmd[cid][1]
                self.db.save_worker_data(worker_id, cmd, data)
                self.db.set_worker_online(worker_id, "Y")
                self.db.set_worker_response_now(worker_id)
            else:
                controller_logger.error("Worker id mismatch.")
        elif cid in self.emergency_cids:
            self.handle_emergency(cid, worker_id, data)
            controller_logger.warning(
                "Get emergency data from {0}.".format(worker_id))
        else:
            controller_logger.error(
                "Time out or unrecognized data.")

        if self._send[worker_id] - self._received[worker_id] >= 3:
            self.db.set_worker_online(worker_id, "N")

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

    def exec_command(self, worker_id, cmd, cid=0):
        """cmd: string command."""
        if not cid:
            cid = self.cid
        cmd_payload = CommandPayload(cmd, cid)
        self.send_cmd(worker_id, cmd_payload)
        self._send[worker_id] += 1
        self.wating_cmd[cid] = (worker_id, cmd)
        self.cid = cid + 1

    def handle_emergency(self, cid, worker_id, data):
        pass

    def run(self):
        self.link.start()


class WatingCommand(collections.UserDict):
    """There is a time limit for data"""

    def __init__(self, *args, time_out=15, **kwargs):
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


if __name__ == "__main__":
    controller = Controller()
    controller.run()
