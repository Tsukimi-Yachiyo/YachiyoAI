import yaml, os, re
import logging

all_yaml = None

logger = logging.getLogger(__name__)

class PersistentYaml:
    def __init__(self):
        self.data = {}
        for yaml_file in os.listdir('resource/config/yaml'):
            with open(f'resource/config/yaml/{yaml_file}', 'r',encoding="utf-8") as f:
                self.data.update(yaml.safe_load(f))

        pattern = re.compile(r'\$\{([a-zA-Z0-9_.]+)}')

        # 递归解析占位符
        def resolve(obj):
            if isinstance(obj, dict):
                return {k: resolve(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [resolve(i) for i in obj]
            if isinstance(obj, str):
                while True:
                    match = pattern.search(obj)
                    if not match:
                        break
                    key_path = match.group(1)
                    keys = key_path.split('.')
                    value = self.data
                    try:
                        for k in keys:
                            value = value[k]
                    except:
                        value = match.group(0)
                    obj = obj.replace(match.group(0), str(value))
                return obj
            return obj

        self.data = resolve(self.data)

    def get(self, key: str, default=None):
        # 支持 a.b.c 层级获取
        keys = key.split('.')
        result = self.data
        try:
            for k in keys:
                result = result[k]
            return result
        except (KeyError, TypeError):
            return default

def yaml_init():
    global all_yaml
    try:
        all_yaml = PersistentYaml()
        logger.info(f"YAML文件加载成功，共加载{len(all_yaml.data)}个键")
    except Exception as e:
        logger.error(f"YAML文件加载失败: {e}")

