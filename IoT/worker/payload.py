# =============================================================================
# Author: falseuser
# File Name: payload.py
# Created Time: 2018-08-30 15:14:42
# Last modified: 2018-09-12 11:23:22
# Description:
# =============================================================================
import json


SUPPORTED_COMMAND = [
    "get_memory_usage",
    "get_time",
]


class CommandPayload(object):
    """ Command payload from Controller to Worker.
    Use a command id to confirm the returned data.
    """

    def __init__(self, command, cid):
        if command not in SUPPORTED_COMMAND:
            raise ValueError("Unsupported command.")
        self.command = command
        self.cid = cid
        self.dict_data = {
            "command": self.command,
            "cid": self.cid,
        }
        self.string = json.dumps(self.dict_data)

    def __repr__(self):
        return "CommandPayload(command: \"{0}\", cid: {1})".format(
            self.command,
            self.cid,
        )

    def __str__(self):
        return self.string


class DataPayload(object):
    """ Data payload from Worker to Controller.
    Respond to the corresponding command with a command id.
    """

    def __init__(self, data, cid):
        self.data = data
        self.cid = cid
        self.dict_data = {
            "data": self.data,
            "cid": self.cid,
        }
        self.string = json.dumps(self.dict_data)

    def __repr__(self):
        return "DataPayload(data: \"{0}\", cid: {1})".format(
            self.data,
            self.cid,
        )

    def __str__(self):
        return self.string
