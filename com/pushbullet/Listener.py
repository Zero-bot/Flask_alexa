#!/usr/bin/env python3

import time
import json
import requests
from com.helpers.ConfigParser import read_config
import websocket


def on_error(ws, error):
    print('Error:', error)


def on_close(ws):
    print('closed')


def on_message(ws, message):
    message = json.loads(message)
    if message["type"] == "tickle" and message["subtype"] == "push":
        print(time.time())
        ten_minutes_ago = str(time.time() - 3 * 60)
        url = "https://api.pushbullet.com/v2/pushes?modified_after="
        print(url + str(ten_minutes_ago) + 'auth=' + api_key)
        data = json.dumps(json.loads(requests.get(url + ten_minutes_ago, auth=(api_key, '')).content.decode('utf8')),
                          indent=2,
                          sort_keys=True)
        print(data)


if __name__ == "__main__":
    websocket.enableTrace(True)
    api_key = read_config("PUSH BULLET", "key")
    ws = websocket.WebSocketApp("wss://stream.pushbullet.com/websocket/" + api_key,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
