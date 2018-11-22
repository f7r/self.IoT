# =============================================================================
# Author: falseuser
# Created Time: 2018-11-21 15:44:59
# Last modified: 2018-11-22 17:48:21
# Description: controller_cmd.py
# =============================================================================
import time
import xmlrpc.client
import json

cmd_proxy = xmlrpc.client.ServerProxy("http://localhost:8088/")


def add_worker(worker_id):
    v = cmd_proxy.add_worker(worker_id)
    if v == 0:
        print("Worker {0} add OK".format(worker_id))
    else:
        print("ERROR")


def remove_worker(worker_id):
    v = cmd_proxy.remove_worker(worker_id)
    if v == 0:
        print("Worker {0} remove OK".format(worker_id))
    else:
        print("ERROR")


def set_worker_config(worker_id, config):
    v = cmd_proxy.set_worker_config(worker_id, config)
    if v == 0:
        print("Worker {0} config set OK".format(worker_id))
    else:
        print("ERROR")


worker_id_list = ["worker1", "worker2", "worker3"]


def add_workers():
    for worker_id in worker_id_list:
        add_worker(worker_id)


def set_workers_config():
    worker1_config = {
        "periodic": {
            "get_cpu_usage": 30,
        }
    }
    config = json.dumps(worker1_config)
    set_worker_config("worker1", config)
    worker2_config = {
        "periodic": {
            "get_cpu_usage": 50,
        }
    }
    config = json.dumps(worker2_config)
    set_worker_config("worker2", config)


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
    add_workers()
    time.sleep(2)
    set_workers_config()
    time.sleep(2)
