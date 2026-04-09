import os,default

# 依赖库(类)
dependencies = default.dependencies

# 修饰器
decorator = {}

# 构建器
builder = {}

# dlc 初始化顺序
init_order = []

# dlc 构建顺序
build_order = []

# 主方法(循环方法)
loop_method = None

# 资源库(用户定义)
resource = {}

# 资源库(系统) - yaml
from resource import yml
resource_yaml = default.resource_yaml | yml.yaml_init()

# 资源库(系统) - json
from resource import json
resource_json = json.json_init()

# 资源库(系统) - env
from resource import config

# 资源库(实例) - 依赖
resource_dependencies = {}

def set_resource(key: str, value: any):
    resource[key] = value

# get 方法
def get_resource(key: str):
    return resource[key]

def get_resource_dependencies(key: str):
    return resource_dependencies[key]

def get_resource_config(key: str):
    return os.getenv(key)

def get_resource_yaml(key: str):
    return resource_yaml[key]

def get_resource_json(key: str):
    return resource_json[key]
