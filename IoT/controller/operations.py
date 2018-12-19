# =============================================================================
# Author: falseuser
# File Name: operations.py
# Created Time: 2018-10-24 15:09:58
# Last modified: 2018-11-28 10:38:37
# Description:
# =============================================================================
import xmlrpc.client


rpc_proxy = xmlrpc.client.ServerProxy("http://localhost:8088/")
OK = "OK"


class ControllerOperations(object):
    """ Mainly database operations.
    """

    def __init__(self):
        pass

    def get_global_config(self):
        return rpc_proxy.get_global_config()

    def set_global_config(self, config):
        v = rpc_proxy.set_global_config(config)
        if v == 0:
            return OK

    def get_workers_id_list(self):
        return rpc_proxy.get_workers_id_list()

    def get_online_workers_id_list(self):
        return rpc_proxy.get_online_workers_id_list()

    def register_worker(self, worker_id, description=""):
        v = rpc_proxy.add_worker(worker_id)
        if v == 0:
            return OK

    def unregister_worker(self, worker_id):
        v = rpc_proxy.remove_worker(worker_id)
        if v == 0:
            return OK


class WorkerOperations(object):
    """ Operation target is specified worker.
    """

    def __init__(self, worker_id):
        self.worker_id = worker_id

    def run_command(self, command):
        pass

    def get_system_info(self):
        pass

    def get_config(self):
        return rpc_proxy.get_worker_config(self.worker_id)

    def get_description(self):
        return rpc_proxy.get_worker_description(self.worker_id)

    def get_supported_commands(self):
        return rpc_proxy.get_supported_commands(self.worker_id)

    def set_config(self, config):
        # config: dict
        v = rpc_proxy.set_worker_config(self.worker_id, config)
        if v == 0:
            return OK

    def reboot(self):
        self.run_command("reboot")

    def shutdown(self):
        self.run_command("shutdown")


class AdminOperations(object):
    """ Mainly operate controller host.
    """

    def __init__(self):
        pass

    def start_broker(self):
        pass

    def stop_broker(self):
        pass

    def restart_broker(self):
        pass

    def get_broker_status(self):
        pass

    def get_broker_log(self):
        pass

    def get_system_info(self):
        pass

    def run_shell_command(self, cmd):
        pass

    def get_controller_log(self):
        pass

    def get_worker_log(self, worker):
        pass
