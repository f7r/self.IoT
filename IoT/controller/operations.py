# =============================================================================
# Author: falseuser
# File Name: operations.py
# Created Time: 2018-10-24 15:09:58
# Last modified: 2018-10-24 16:43:30
# Description:
# =============================================================================


class ControllerOperations(object):
    """ Mainly database operations.
    """

    def __init__(self):
        pass

    def get_summary_status(self):
        pass

    def get_registered_workers(self):
        pass

    def get_online_workers(self):
        pass

    def get_offline_workers(self):
        pass

    def get_global_config(self):
        pass

    def get_worker_config(self, worker):
        pass

    def set_worker_config(self, worker):
        pass

    def get_worker_status(self, worker):
        # Include worker id, system info, supported commands.
        pass

    def register_worker(self, worker):
        pass

    def unregister_worker(self, worker):
        pass

    def set_global_config(self, config):
        pass


class WorkerOperations(object):
    """ Mainly by run command operation.
    """

    def __init__(self):
        pass

    def run_command(self, command):
        pass

    def get_system_info(self):
        pass

    def get_supported_commands(self):
        pass

    def reboot(self):
        pass

    def shutdown(self):
        pass


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
