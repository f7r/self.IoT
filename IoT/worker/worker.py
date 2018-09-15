# =============================================================================
# Author: falseuser
# File Name: worker.py
# Created Time: 2018-09-07 18:00:22
# Last modified: 2018-09-15 18:14:54
# Description:
# =============================================================================
import time
from link import WorkerLink
from commands import CMD_FUNC_MAP
from worker_utils import config, worker_logger
from payload import CommandPayload, DataPayload


class Worker(object):

    def __init__(self):
        worker_id = config.get("default", "worker_id")
        parent_topic = config.get("mqtt", "parent_topic")
        self.link = WorkerLink(worker_id, parent_topic)
        self.link.processing = self.processing

    def processing(self, payload):
        """ Worker processing function.
        Data type:
            payload: string.
        """
        try:
            cmd_payload = CommandPayload.load(payload)
        except Exception as e:
            worker_logger.exception(e)
            return
        cmd = cmd_payload.command
        args = cmd_payload.args
        cid = cmd_payload.cid
        func = CMD_FUNC_MAP[cmd]
        data = func(args)
        data_payload = DataPayload(data, cid)
        self.send_data(data_payload)

    def send_data(self, data_payload):
        """ Worker send function.
        Data type:
            data_payload: DataPayload instance.
        """
        payload = data_payload.string
        rc = self.link.send(payload)
        if rc == 0:
            worker_logger.info(
                "Data(cid={0}) send succeeded.".format(data_payload.cid))
        else:
            worker_logger.warning(
                "Data(cid={0}) send failed.".format(data_payload.cid))

    def run(self):
        self.link.start()
        worker_logger.info("Worker started.")
        while True:
            time.sleep(1)


if __name__ == "__main__":
    s = Worker()
    s.run()
