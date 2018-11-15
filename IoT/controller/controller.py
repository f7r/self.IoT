# =============================================================================
# Author: falseuser
# Created Time: 2018-11-15 17:11:34
# Last modified: 2018-11-15 17:50:55
# Description: controller.py
# =============================================================================
from link import ControllerLink
from controller_utils import config, controller_logger
from payload import CommandPayload, DataPayload


class Controller(object):

    def __init__(self):
        controller_id = config.get("default", "controller_id")
        parent_topic = config.get("mqtt", "parent_topic")
        self.link = ControllerLink(controller_id, parent_topic)
        self.link.processing = self.processing

    def processing(self, payload):
        """payload: string"""
        try:
            data_payload = DataPayload.load(payload)
        except Exception as e:
            controller_logger.exception(e)
            return
        data = data_payload.data
        cid = data_payload.cid

    def send_cmd(self, cmd_payload):
        """cmd_payload: CommandPayload instance."""
        payload = cmd_payload.string

    def run(self):
        pass


if __name__ == "__main__":
    pass
