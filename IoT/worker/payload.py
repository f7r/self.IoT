# =============================================================================
# Author: falseuser
# File Name: payload.py
# Created Time: 2018-08-30 15:14:42
# Last modified: 2018-09-15 18:04:04
# Description:
# =============================================================================
import json
from commands import CMD_FUNC_MAP


class CommandPayload(object):
    """ Command payload from Controller to Worker.
    Use a command id to confirm the returned data.
    """

    def __init__(self, command, args, cid):
        if command not in CMD_FUNC_MAP:
            raise ValueError("Unsupported command.")
        self.command = command
        self.args = args
        self.cid = cid
        self.dict_data = {
            "command": self.command,
            "args": self.args,
            "cid": self.cid,
        }
        self.string = json.dumps(self.dict_data)

    @classmethod
    def load(cls, payload):
        payload_dict = json.loads(payload)
        command = payload_dict['command']
        args = payload_dict['args']
        cid = payload_dict['cid']
        return cls(command, args, cid)

    def __repr__(self):
        return "CommandPayload(\
command: \"{0}\", args: \"{1}\", cid: {2})".format(
            self.command,
            self.args,
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

    @classmethod
    def load(cls, payload):
        payload_dict = json.loads(payload)
        data = payload_dict['data']
        cid = payload_dict['cid']
        return cls(data, cid)

    def __repr__(self):
        return "DataPayload(data: \"{0}\", cid: {1})".format(
            self.data,
            self.cid,
        )

    def __str__(self):
        return self.string
