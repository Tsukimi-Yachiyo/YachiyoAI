"""
    # 嵌入 插件
    提供嵌入功能，将所有依赖项和装饰器加载到全局命名空间中
"""
logger = logging.getLogger(__name__)

class Main(BaseMain):

    init_order = -10

    def __init__(self):
        self.build()

    def build(self):
        __builtins__["library"] = library
        plugin_count = 0

        for classes in library.dependencies.keys():
            for module in library.dependencies[classes].keys():
                __builtins__[classes+module] = library.dependencies[classes][module]
                plugin_count += 1

        for decorator in library.decorator.keys():
            __builtins__[decorator] = library.decorator[decorator]
            plugin_count += 1

        for yml in library.resource_yaml.keys():
            __builtins__[yml.replace(".", "_")] = library.resource_yaml[yml]
            plugin_count += 1

        for json in library.resource_json.keys():
            __builtins__[json] = library.resource_json[json]
            plugin_count += 1
        logger.info(f"嵌入 {plugin_count} 个插件")
