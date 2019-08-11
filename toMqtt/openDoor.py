#!/usr/bin/env python3
import configparser
import json
import os
import sys

import paho.mqtt.publish as publish

def agi_exit(rc, *args):
    if rc != 0:
        print("VERBOSE rc=%s %s" % (rc, args))
    sys.exit(rc)


def run():
    config_file = os.path.splitext(__file__)[0] + ".conf"

    config = configparser.ConfigParser()
    config.read(config_file)

    mqtt_server = config.get('mqtt', 'server')
    mqtt_port = config.getint('mqtt', 'port', fallback=1883)
    mqtt_username = config.get('mqtt', 'username', fallback=None)
    mqtt_password = config.get('mqtt', 'password', fallback=None)
    mqtt_topic = config.get('mqtt', 'topic')

    try:
        auth = {}
        if mqtt_username is not None and mqtt_password is not None:
            auth = {
                'username': mqtt_username,
                'password': mqtt_password
            }
        publish.single(mqtt_topic, payload="4000",
                       hostname=mqtt_server, port=mqtt_port, auth=auth)
    except Exception as e:
        agi_exit(1, "Connection failed: %s" % str(e))

    agi_exit(0)


if __name__ == '__main__':
    run()
