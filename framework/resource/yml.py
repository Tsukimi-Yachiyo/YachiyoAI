import yaml, os, re
import logging


logger = logging.getLogger(__name__)
yaml_file_dir = 'resource/yaml'

def yaml_init():
    data = {}
    for yaml_file in os.listdir(yaml_file_dir):
        if yaml_file.endswith('.yml') or yaml_file.endswith('.yaml'):
            with open(f'{yaml_file_dir}/{yaml_file}', 'r',encoding="utf-8") as f:
                data.update(yaml.safe_load(f))

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
                value = data
                try:
                    for k in keys:
                        value = value[k]
                except:
                    value = match.group(0)
                obj = obj.replace(match.group(0), str(value))
            return obj
        return obj
    data = resolve(data)

    # 将嵌套字典转换为扁平字典
    def flatten(obj, parent_key='', sep='.'):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f'{parent_key}{sep}{k}' if parent_key else k
                items.extend(flatten(v, new_key, sep).items())
        else:
            items.append((parent_key, obj))

        return dict(items)
    data = flatten(data)
    return data