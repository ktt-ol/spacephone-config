#!/usr/bin/env python3
import configparser
import json
import os
import sys

import paho.mqtt.publish as publish

relevant_agi_data = ["agi_callerid", "agi_calleridname", "agi_dnid", "agi_context", "agi_extension"]


def agi_exit(rc, *args):
    if rc != 0:
        print("VERBOSE rc=%s %s" % (rc, args))
    sys.exit(rc)


def run():
    global relevant_agi_data
    config_file = os.path.splitext(__file__)[0] + ".conf"

    config = configparser.ConfigParser()
    config.read(config_file)

    mqtt_server = config.get('mqtt', 'server')
    mqtt_port = config.getint('mqtt', 'port', fallback=1883)
    mqtt_username = config.get('mqtt', 'username', fallback=None)
    mqtt_password = config.get('mqtt', 'password', fallback=None)
    mqtt_topic = config.get('mqtt', 'topic')

    agi = {}
    while 1:
        line = sys.stdin.readline()
        if not line or line == "\n":
            break
        split = line.rstrip('\n').split(': ', 1)
        if split[0] in relevant_agi_data:
            if len(split) < 2:
                split = [split[0], ""]
            agi[split[0]] = split[1]

    if len(sys.argv) > 1:
        agi['agi_extension'] = sys.argv[1]

    try:
        auth = {}
        if mqtt_username is not None and mqtt_password is not None:
            auth = {
                'username': mqtt_username,
                'password': mqtt_password
            }
        publish.single(mqtt_topic, payload=json.dumps(agi),
                       hostname=mqtt_server, port=mqtt_port, auth=auth)
    except Exception as e:
        agi_exit(1, "Connection failed: %s" % str(e))

    agi_exit(0)


if __name__ == '__main__':
    run()
