# =============================================================================
# Author: falseuser
# File Name: link.py
# Created Time: 2018-08-29 16:38:37
# Last modified: 2018-11-15 17:30:41
# Description:
# =============================================================================
import paho.mqtt.client as mqtt
# from configure import CONFIG
from controller_utils import link_logger, controller_logger, config


class ControllerLink(object):

    def __init__(self, client_id, parent_topic):
        self.client_id = client_id
        self.data_topic = "{0}/{1}/data".format(parent_topic, client_id)
        self.cmd_topic = "{0}/{1}/cmd".format(parent_topic, client_id)
        self.status_id = 255
        self.status_msg = ""
        self.userdata = ""
        self.config_link()

    def config_link(self):
        self.client = mqtt.Client(client_id=self.client_id)
        if config.getboolean("mqtt", "use_tls"):
            self.client.tls_set(
                ca_certs=config.get("mqtt", "tls_ca_file"),
                certfile=config.get("mqtt", "tls_cert_file"),
                keyfile=config.get("mqtt", "tls_key_file"),
            )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_publish = self.on_publish
        self.client.enable_logger(link_logger)
        self.client.connect(
            host=config.get("mqtt", "broker_host"),
            port=config.getint("mqtt", "broker_port"),
            keepalive=config.getint("mqtt", "keepalive"),
        )

    def on_connect(self, client, userdata, flags, rc):
        """Subscribe to data topic."""
        self.client.subscribe(
            topic=self.data_topic,
            qos=2,
        )
        self.status_id = rc
        if self.status_id == 0:
            controller_logger.info("Connection succeeded.")

    def on_message(self, client, userdata, msg):
        self.processing(msg.payload)

    def on_publish(self, client, userdata, mid):
        pass

    def send(self, payload):
        """Send command payload to command topic."""
        cmd_info = self.client.publish(
            topic=self.cmd_topic,
            payload=payload,
            qos=2,
        )
        self.last_mid = cmd_info.mid
        self.status_id = cmd_info.rc
        return cmd_info.rc

    def processing(self, payload):
        # This function should implement in subclass or use Monkey Patch.
        raise NotImplementedError

    def start(self):
        return self.client.loop_start()

    def stop(self):
        return self.client.loop_stop()

    def keep(self):
        return self.client.loop_forever()
