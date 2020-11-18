import json
import socket
import sys

import cv2




class App:
    __slots__ = ("__saddr")
    def __init__(self, saddr):
        self.__saddr = saddr

    def run(self):
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, frame = camera.read()
            data = cv2.imencode(".jpeg", frame)[1].tobytes()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(self.__saddr)
            client.send(data)


def main():
    settings_path = "./client.json"
    if len(sys.argv) >= 2:
        settings_path = sys.argv[1]

    try:
        with open(settings_path, "r") as fistream:
            data = json.load(fistream)
        App(
            saddr=(data["server"]["ip"], data["server"]["port"])
        ).run()

    except FileNotFoundError:
        with open(settings_path, "w") as fostream:
            json.dump({"server": {"ip": "127.0.0.1", "port": 8080}}, fostream)
        print("Settings file not found, new was created. Configure it")
    except KeyError as err:
        print(f"Parameter '{str(err)}' unfilled in settings file")


if __name__ == '__main__':
    main()
