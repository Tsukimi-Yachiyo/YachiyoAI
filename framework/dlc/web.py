"""
    # Web 服务 插件
    提供 Web 服务的构建和运行功能

"""


from fastapi import FastAPI
import uvicorn

logger = logging.getLogger(__name__)

# 检查服务配置文件是否存在
def _check():
    import os
    if not os.path.exists("resource\\yaml\\service.yaml") and not os.path.exists("resource\\yaml\\service.yml"):
        logger.error("service.yaml 或 service.yml 文件不存在")
        raise FileNotFoundError("service.yaml 或 service.yml 文件不存在")

"""
     Web 服务 主类
"""
class Main(BaseMain):

    def __init__(self):
        _check()
        library.dependencies["PostController"] = {}
        library.dependencies["GetController"] = {}
        library.dependencies["PostAutoController"] = {}
        library.dependencies["GetAutoController"] = {}
        library.resource["path"] = {}

        self.service_title = library.resource_yaml["service.title"]
        self.service_version = library.resource_yaml["service.version"]
        self.service_host = library.resource_yaml["service.host"]
        self.service_port = library.resource_yaml["service.port"]
        # 构建所有控制器实例
        self.app = FastAPI(title=self.service_title, version=self.service_version)

    def build(self):
        for name, func in library.dependencies["PostController"].items():
            self.app.add_api_route(library.resource["path"][name], func, methods=["POST"])
        for name, func in library.dependencies["GetController"].items():
            self.app.add_api_route(library.resource["path"][name], func, methods=["GET"])
        for name, func in library.dependencies["PostAutoController"].items():
            self.app.add_api_route(library.resource["path"][name], func, methods=["POST"])
        for name, func in library.dependencies["GetAutoController"].items():
            self.app.add_api_route(library.resource["path"][name], func, methods=["GET"])

    def loop_method(self):
        logger.info(f"启动服务 {self.service_title}，监听地址 {self.service_host}:{self.service_port}")
        uvicorn.run(self.app, host=self.service_host, port=self.service_port)
        logger.info("服务启动成功")

"""
    post 控制器装饰器
    用于定义 post 请求的控制器
    :param path: 控制器路径
    :param name: 控制器名称
    :return: 控制器实例
"""
def post_controller(path: str, name: str = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.resource["path"][name] = path
        library.dependencies["PostController"][name] = func
        logger.info(f"PostController {name} 已加入库")
        return func
    return decorator

"""
    get 控制器方法装饰器
    用于定义 get 请求的控制器方法
    :param path: 控制器路径
    :param name: 控制器名称
    :return: 控制器方法实例
"""
def get_controller(path: str, name: str = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.resource["path"][name] = path
        library.dependencies["GetController"][name] = func
        logger.info(f"GetController {name} 已加入库")
        return func
    return decorator

"""
    post 自动填充参数控制器方法装饰器
    用于定义 post 请求的控制器方法，自动填充参数
    :param path: 控制器路径
    :param name: 控制器名称
    :return: 控制器方法实例
"""
def post_auto_controller(path: str, name: str = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.resource["path"][name] = path
        library.dependencies["PostAutoController"][name] = func
        logger.info(f"PostAutoController {name} 已加入库")
        return func
    return decorator

"""
    get 自动填充参数控制器方法装饰器
    用于定义 get 请求的控制器方法，自动填充参数
    :param path: 控制器路径
    :param name: 控制器名称
    :return: 控制器方法实例
"""
def get_auto_controller(path: str, name: str = None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        library.resource["path"][name] = path
        library.dependencies["GetAutoController"][name] = func
        logger.info(f"GetAutoController {name} 已加入库")
        return func
    return decorator
