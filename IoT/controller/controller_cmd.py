# =============================================================================
# Author: falseuser
# Created Time: 2018-11-21 15:44:59
# Last modified: 2018-11-21 16:42:57
# Description: controller_cmd.py
# =============================================================================
import xmlrpc.client

cmd_proxy = xmlrpc.client.ServerProxy("http://localhost:8088/")


def add_worker(worker_id):
    v = cmd_proxy.add_worker(worker_id)
    if v == 0:
        print("OK")
    else:
        print("ERROR")

def remove_worker(worker_id):
    v = cmd_proxy.remove_worker(worker_id)
    if v == 0:
        print("OK")
    else:
        print("ERROR")

def get_workers():
    v = cmd_proxy.get_workers()
    print(v)


if __name__ == "__main__":
    import pdb;pdb.set_trace()
    print(1)
    print(2)
