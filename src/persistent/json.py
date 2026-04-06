from json import loads, dumps
import os

logger = logging.getLogger(__name__)
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
    try:
        all_json = PersistentJson()
        logger.info(f"JSON文件加载成功，共加载{len(all_json.data)}个键")
    except Exception as e:
        logger.error(f"JSON文件加载失败: {e}")
