from json import loads, dumps
import os

all_json = None

class PersistentJson:

    def __init__(self):
        self.data = {}
        for json in os.listdir('resource/json'):
            with open(f'resource/json/{json}', 'r',encoding="utf-8") as f:
                self.data[json.split('.')[0]] = loads(f.read())

    def get(self, key: str):
        return self.data.get(key, None)

def json_init():
    global all_json
    all_json = PersistentJson()
